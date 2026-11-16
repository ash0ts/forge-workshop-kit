# Share a workshop

Use the [sharing page](https://ash0ts.github.io/forge-workshop-kit/share/) to copy a tracked link or download a QR code. Use the [Slack collection link](https://utm.io/uuIac) in a Slack message and the [Loom collection link](https://utm.io/uuIan) in the recording's description and closing screen. Both open the same packet, with different source attribution. Each workshop also has its own link, which opens that workshop's card in the packet.

The destination includes the illustrated example, deck, facilitator instructions, and notebook. People can read the introduction before signing in. Running the notebook uses their own Forge project and credentials.

## Put the code where someone can use it

- Show the workshop QR when introducing the session and when wrapping up. Keep it visible while people open the page.
- Use the same workshop QR on its poster or handout. Keep the white border, preserve its square shape, and include the written short link for people who cannot scan it.
- Share the Slack collection link with the meeting brief. Use the Loom link with the [ten-minute walkthrough](loom-walkthrough.md), and a workshop link when the invitation names one session.
- Keep the direct notebook link beside the copy instructions. The sharing link leads to the public introduction; the notebook link opens Forge and may ask the participant to sign in.

Download PNG for a message and SVG for a slide or print layout. Both encode the same registered short URL. Do not replace the destination with a local preview address or a facilitator's notebook copy.

## How tracking works

[share-links.json](share-links.json) is the source for registered UTM.io short links and their full destinations. All use the campaign `2026-q4_global_forge-workshop-kit`.

| Placement | `utm_source` | `utm_medium` | `utm_content` |
| --- | --- | --- | --- |
| Workshop deck, poster, or invitation | `forge-workshop-kit` | `workshop` | `<workshop>-start` |
| Slack collection message | `slack` | `social` | `meeting-packet` |
| Loom description and closing screen | `loom` | `video` | `kit-walkthrough` |

A workshop uses one link across its deck and poster. These links therefore identify the workshop, not the particular surface that someone scanned. Verification clicks, repeat visits, and link previews are not attendee counts. UTM parameters describe the incoming link; they do not establish that someone copied or completed a notebook.

Read UTM.io link activity separately from the facilitator's progress monitor. The monitor reads updates from projects on the facilitator's roster; it does not join those updates to anonymous link clicks. For an event or placement that needs separate attribution, register a new link instead of reusing the Slack or Loom link and calling those visits event traffic.

## Update a destination

Create or update the link in UTM.io, then record its short URL and full destination in the manifest. Query parameters go before the workshop fragment, for example `?utm_source=…#solar`. Keep existing short URLs when refreshing material so printed posters continue to work.

The regular deck build regenerates QR assets from the manifest. To check or regenerate them separately:

```sh
python scripts/build_share_links.py --check
python scripts/build_share_links.py --site dist/decks/site
```

The build validates the destination and tracking fields, then writes the deck QR assets, poster links, and public sharing page. It uses the visual skill's pinned QR dependency and makes no network requests. After publication, scan each code and check the redirected URL, workshop card, and notebook link. Local generation cannot verify a UTM.io redirect or Forge access.

For the session itself, use the [facilitator instructions](facilitator-start.md) and the workshop's run guide in the [packet](https://ash0ts.github.io/forge-workshop-kit/packet/).
