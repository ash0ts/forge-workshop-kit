import fs from 'node:fs/promises'
import path from 'node:path'
import { pathToFileURL } from 'node:url'
import MarkdownIt from '../decks/node_modules/markdown-it/index.mjs'
import { chromium } from '../decks/node_modules/playwright/index.mjs'

const mode = process.argv[2]
if (mode === 'markdown') {
  let input = ''
  for await (const chunk of process.stdin) input += chunk
  const result = {}
  for (const doc of JSON.parse(input)) {
    const md = new MarkdownIt({html: false, linkify: true})
    const renderLink = md.renderer.rules.link_open || ((tokens, idx, opts, env, self) => self.renderToken(tokens, idx, opts))
    md.renderer.rules.link_open = (tokens, idx, opts, env, self) => {
      const href = tokens[idx].attrGet('href')
      if (href && !/^(?:[a-z][a-z0-9+.-]*:|#)/i.test(href)) {
        const [relative, fragment] = href.split('#')
        const source = path.posix.normalize(path.posix.join(path.posix.dirname(doc.path), relative))
        const destination = doc.bundled[source]
        const resolved = destination
          ? path.posix.relative(path.posix.dirname(doc.output), destination) + (fragment ? '#' + fragment : '')
          : new URL(href, doc.base + doc.path).href
        tokens[idx].attrSet('href', resolved)
      }
      return renderLink(tokens, idx, opts, env, self)
    }
    md.renderer.rules.heading_open = (tokens, idx, opts, env, self) => {
      const content = tokens[idx + 1].content
      tokens[idx].attrSet('id', content.toLowerCase().replace(/[^\p{L}\p{N}\s-]/gu, '').replace(/\s+/g, '-'))
      return self.renderToken(tokens, idx, opts)
    }
    result[doc.id || doc.path] = md.render(doc.text).replaceAll('<pre>', '<pre tabindex="0" aria-label="Code example">').replaceAll('<table>', '<table tabindex="0">')
  }
  process.stdout.write(JSON.stringify(result))
} else if (mode === 'pdf') {
  const source = path.resolve(process.argv[3])
  const printSource = source.replace(/\.html$/, '.print.html')
  const canonical = process.argv[5]
  if (!canonical) throw new Error('PDF export requires its public page URL')
  const markup = (await fs.readFile(source, 'utf8')).replace(/<a href="([^"]+)"/g, (_, href) =>
    '<a href="' + new URL(href, canonical).href + '"')
  await fs.writeFile(printSource, markup)
  const browser = await chromium.launch({headless: true, ...(process.env.CHROME_PATH ? {executablePath:process.env.CHROME_PATH} : {})})
  try {
    const page = await browser.newPage()
    await page.goto(pathToFileURL(printSource).href)
    await page.evaluate(() => document.fonts.ready)
    await page.pdf({path: path.resolve(process.argv[4]), format:'Letter', printBackground:true,
      margin:{top:'0.65in', bottom:'0.65in', left:'0.65in', right:'0.65in'},
      displayHeaderFooter:true, headerTemplate:'<span></span>',
      footerTemplate:'<div style="font:9px sans-serif;width:100%;text-align:center;color:#60625d">Forge Workshop Kit · Meeting packet · <span class="pageNumber"></span></div>'})
  } finally { await browser.close(); await fs.rm(printSource, {force:true}) }
} else { throw new Error('Use markdown or pdf mode') }
