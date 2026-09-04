# Set checkout logo

`update_checkout_customization` does not set the logo. Use `set_checkout_logo`: mint, PUT the bytes, confirm.

The developer needs a local image: png, jpeg, or webp, ≤ 5 MB. Ask for the file path if they have not given one.

## 1. Mint

Call `set_checkout_logo` with:
- `action`: `"mint"`
- `merchantId`
- `fileName`: the file name (e.g. `logo.png`)
- `contentType`: `image/png` | `image/jpeg` | `image/jpg` | `image/webp`

Returns `{ uploadUrl, path, expiresAt }`.

## 2. PUT the file

HTTP PUT the file bytes to `uploadUrl` with that same `Content-Type`. The image bytes never go through the tool.

Complete when the PUT succeeds.

## 3. Confirm

Call `set_checkout_logo` with:
- `action`: `"confirm"`
- `merchantId`
- `path`: the exact `path` from mint

Returns `{ logoUrl }`. Present it. Complete when `logoUrl` is on screen.

Replaces any existing checkout logo. Clearing a logo is done from the dashboard, not this tool.
