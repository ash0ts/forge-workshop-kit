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
} else if (mode === 'check') {
  const site = path.resolve(process.argv[3])
  const output = path.resolve(process.argv[4])
  await fs.mkdir(output, {recursive:true})
  const sources = ['index.html', 'visual-language/index.html', ...[
    'pending', 'solar', 'routing', 'inspection', 'transit', 'airline_monitoring',
  ].map(slug => `packet/start/${slug}.html`)]
  const results = []
  const browser = await chromium.launch({headless:true, ...(process.env.CHROME_PATH ? {executablePath:process.env.CHROME_PATH} : {})})
  try {
    for (const width of [1280, 390]) {
      const page = await browser.newPage({viewport:{width, height:844}, reducedMotion:'reduce'})
      for (const source of sources) {
        await page.goto(pathToFileURL(path.join(site, source)).href, {waitUntil:'domcontentloaded'})
        await page.evaluate(async () => {
          await document.fonts.ready
          await Promise.all([...document.images].map(image => {
            image.loading = 'eager'
            return image.decode().catch(() => {})
          }))
        })
        const result = await page.evaluate(() => {
          const issues = []
          const visible = element => {
            const style = getComputedStyle(element)
            return style.display !== 'none' && style.visibility !== 'hidden' && element.getClientRects().length > 0
          }
          for (const image of document.images) {
            if (!image.complete || !image.naturalWidth) issues.push({kind:'image', source:image.getAttribute('src')})
          }
          const skip = document.querySelector('a.skip')
          if (skip) {
            skip.focus()
            const rect = skip.getBoundingClientRect()
            if (rect.left < -2 || rect.right > innerWidth + 2) issues.push({kind:'hidden-focused-skip-link'})
            skip.blur()
          }
          const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT)
          while (walker.nextNode()) {
            const node = walker.currentNode
            const element = node.parentElement
            if (!node.textContent.trim() || !element || !visible(element) || element.closest('script,style,a.skip')) continue
            // Code and tables deliberately scroll horizontally on small screens.
            const scrollable = element.closest('pre,table')
            const range = document.createRange()
            range.selectNodeContents(node)
            for (const rect of range.getClientRects()) {
              if (!rect.width || !rect.height) continue
              if (!scrollable && (rect.left < -2 || rect.right > innerWidth + 2)) {
                issues.push({kind:'viewport-text', text:node.textContent.trim().slice(0,120), left:rect.left, right:rect.right})
              }
              for (let parent = element; parent && parent !== document.body; parent = parent.parentElement) {
                const style = getComputedStyle(parent)
                const box = parent.getBoundingClientRect()
                const clipsX = ['hidden','clip'].includes(style.overflowX)
                const clipsY = ['hidden','clip'].includes(style.overflowY)
                if ((clipsX && (rect.left < box.left - 2 || rect.right > box.right + 2)) ||
                    (clipsY && (rect.top < box.top - 2 || rect.bottom > box.bottom + 2))) {
                  issues.push({kind:'clipped-text', text:node.textContent.trim().slice(0,120), parent:parent.tagName})
                  break
                }
              }
            }
          }
          return {title:document.title, actual_width:innerWidth, issues}
        })
        const screenshot = source.replaceAll('/', '-').replace('.html', `-${width}.png`)
        await page.screenshot({path:path.join(output, screenshot), fullPage:true})
        results.push({source, width, screenshot, ...result})
      }
      await page.close()
    }
  } finally { await browser.close() }
  const receipt = {pages:results.length, issues:results.flatMap(row => row.issues.map(issue => ({source:row.source,width:row.width,...issue}))), results}
  await fs.writeFile(path.join(output, 'site-checks.json'), JSON.stringify(receipt,null,2) + '\n')
  console.log(JSON.stringify({pages:receipt.pages, issues:receipt.issues},null,2))
  if (receipt.issues.length) process.exitCode = 1
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
      footerTemplate:'<div style="font:9px sans-serif;width:100%;text-align:center;color:#60625d">Forge Workshop Kit · Workshop guide · <span class="pageNumber"></span></div>'})
  } finally { await browser.close(); await fs.rm(printSource, {force:true}) }
} else { throw new Error('Use markdown, check, or pdf mode') }
