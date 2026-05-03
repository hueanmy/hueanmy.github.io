import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';

const isDev = process.argv[2] === 'dev';

const extraIntegrations = [];
let output = 'static';

if (isDev) {
  const react = (await import('@astrojs/react')).default;
  const keystatic = (await import('@keystatic/astro')).default;
  extraIntegrations.push(react(), keystatic());
  output = 'static';
}

export default defineConfig({
  site: 'https://hueanmy.github.io',
  output,
  integrations: [mdx(), sitemap(), ...extraIntegrations],
});
