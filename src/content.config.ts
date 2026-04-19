import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const extensions = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/extensions' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    platform: z.enum(['vscode', 'chrome', 'firefox', 'jetbrains', 'raycast', 'other']),
    demoUrl: z.string().url().optional(),
    installUrl: z.string().url().optional(),
    repoUrl: z.string().url().optional(),
    installs: z.number().optional(),
    order: z.number().default(0),
  }),
});

const projects = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/projects' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    repoUrl: z.string().url().optional(),
    demoUrl: z.string().url().optional(),
    tech: z.array(z.string()).default([]),
    featured: z.boolean().default(false),
    order: z.number().default(0),
  }),
});

export const collections = { extensions, projects };
