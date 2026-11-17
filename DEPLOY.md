# Deploy terryennison.studio

The simplest free host for this site is GitHub Pages. The repo is already a folder of static files, and the `CNAME` file at the root contains `terryennison.studio`. GitHub Pages reads that file and treats the apex domain as the canonical address. `www.terryennison.studio` then redirects to it.

Cloudflare Pages and Netlify can host the same files. They do not need the `CNAME` file, and leaving it in the repo does not affect them.

## GitHub Pages

1. Push this folder to a public GitHub repository.
2. In the repository, open Settings, then Pages.
3. Under Build and deployment, set the source to Deploy from a branch. Choose the branch that holds these files, and set the folder to `/ (root)`.
4. Under Custom domain, enter `terryennison.studio` and save. GitHub will keep the `CNAME` file in sync with that value.
5. After DNS is in place, turn on Enforce HTTPS. The checkbox can take up to a day to become available.

Replace `USERNAME` below with the GitHub username (or organization) that owns the repository. The record must point at `USERNAME.github.io`, not at `USERNAME.github.io/repository`.

### DNS records

Add every record. Remove any existing A, AAAA, or CNAME records on the apex and on `www` before you add these, including a parked-domain record from the registrar.

| Type | Name | Value |
| --- | --- | --- |
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| AAAA | `@` | `2606:50c0:8000::153` |
| AAAA | `@` | `2606:50c0:8001::153` |
| AAAA | `@` | `2606:50c0:8002::153` |
| AAAA | `@` | `2606:50c0:8003::153` |
| CNAME | `www` | `USERNAME.github.io` |

If the DNS host supports an ALIAS or ANAME record and you prefer that to the four A records, point `@` at `USERNAME.github.io` instead of the A and AAAA rows. Keep the `www` CNAME either way.

Check from a terminal:

```bash
dig terryennison.studio +noall +answer -t A
dig terryennison.studio +noall +answer -t AAAA
dig www.terryennison.studio +nostats +nocomments +nocmd
```

The apex answers should be the four A addresses and the four AAAA addresses above. The `www` answer should be a CNAME to `USERNAME.github.io`.

DNS can take up to 24 hours to propagate. Add the custom domain in the GitHub Pages settings before you change DNS, so the domain is not left pointing at GitHub with no site attached.

## If you use Cloudflare Pages instead

Create a Pages project, set the build command to none, and set the output directory to the repository root.

In the DNS panel for `terryennison.studio`:

| Type | Name | Value | Proxy |
| --- | --- | --- | --- |
| CNAME | `@` | `YOUR-PROJECT.pages.dev` | DNS only, or proxied |
| CNAME | `www` | `YOUR-PROJECT.pages.dev` | DNS only, or proxied |

Cloudflare allows a CNAME on the apex. In the Pages project, add both `terryennison.studio` and `www.terryennison.studio` as custom domains, and set the apex as the primary so `www` redirects to it.
