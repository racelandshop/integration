{%- if version_installed == "main" %}

## You are running main!

This is **only** intended for development!

{%- elif (version_installed.split(".")[0] | int) < 1 %}

# Breaking changes!

Read the release notes!
https://github.com/racelandshop/integration/releases/tag/1.0.0
{% endif %}

## Useful links

- [General documentation](https://racelandshop.xyz/)
- [Configuration](https://racelandshop.xyz/docs/configuration/start)
- [FAQ](https://racelandshop.xyz/docs/faq/what)
- [GitHub](https://github.com/racelandshop)
- [Discord](https://discord.gg/apgchf8)
- [Become a GitHub sponsor? ❤️](https://github.com/sponsors/ludeeus)
- [BuyMe~~Coffee~~Beer? 🍺🙈](https://buymeacoffee.com/ludeeus)
