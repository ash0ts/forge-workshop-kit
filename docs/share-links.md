# Share a workshop

Use the [sharing page](https://ash0ts.github.io/forge-workshop-kit/share/) to copy a tracked link or download a QR code. The collection link is for a Slack message or meeting about all six workshops. Each workshop also has its own link, which opens that workshop's card in the public packet.

The destination includes the illustrated example, deck, facilitator instructions, and notebook. People can read the introduction before signing in. Running the notebook uses their own Forge project and credentials.

## Put the code where someone can use it

- Show the workshop QR when introducing the session and when wrapping up. Keep it visible while people open the page.
- Use the same workshop QR on its poster or handout. Keep the white border, preserve its square shape, and include the written short link for people who cannot scan it.
- Share the collection link with the meeting brief. Use a workshop link when the invitation names one session.
- Keep the direct notebook link beside the copy instructions. The sharing link leads to the public introduction; the notebook link opens Forge and may ask the participant to sign in.

Download PNG for a message and SVG for a slide or print layout. Both encode the same registered short URL. Do not replace the destination with a local preview address or a facilitator's notebook copy.

## How tracking works

[share-links.json](share-links.json) is the source for registered UTM.io short links and their full destinations. Workshop links use `utm_source=forge-workshop-kit`, `utm_medium=workshop`, and `utm_content=<workshop>-start`. The collection link uses `utm_source=slack`, `utm_medium=social`, and `utm_content=meeting-packet`. Their campaign comes from the manifest.

A workshop uses one link across its deck and poster. These links therefore identify the workshop, not the particular surface that someone scanned. Verification clicks, repeat visits, and link previews are not attendee counts. UTM parameters describe the incoming link; they do not establish that someone copied or completed a notebook.

## Update a destination

Create or update the link in UTM.io, then record its short URL and full destination in the manifest. Query parameters go before the workshop fragment, for example `?utm_source=…#solar`. Keep existing short URLs when refreshing material so printed posters continue to work.

The regular deck build regenerates QR assets from the manifest. To check or regenerate them separately:

```sh
python scripts/build_share_links.py --check
python scripts/build_share_links.py --site dist/decks/site
```

The build validates the destination and tracking fields, then writes the deck QR assets, poster links, and public sharing page. It uses the visual skill's pinned QR dependency and makes no network requests. After publication, scan each code and check the redirected URL, workshop card, and notebook link. Local generation cannot verify a UTM.io redirect or Forge access.

For the session itself, use the [facilitator instructions](facilitator-start.md) and the workshop's run guide in the [packet](https://ash0ts.github.io/forge-workshop-kit/packet/).
