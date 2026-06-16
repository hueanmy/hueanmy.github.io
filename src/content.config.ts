import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const extensions = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/extensions' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    platform: z.enum(['vscode', 'chrome', 'firefox', 'jetbrains', 'raycast', 'other']),
    demoUrl: z.string().url().optional(),
    videoUrl: z.string().optional(),
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
    description_en: z.string().optional(),
    repoUrl: z.string().url().optional(),
    demoUrl: z.string().url().optional(),
    tech: z.array(z.string()).default([]),
    featured: z.boolean().default(false),
    order: z.number().default(0),
  }),
});

const courses = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/courses' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    description_en: z.string().optional(),
    tagline: z.string().optional(),
    video: z.string().optional(),
    videoFull: z.string().optional(),
    thumbnail: z.string().optional(),
    duration: z.string().optional(),
    date: z.coerce.date().optional(),
    tags: z.array(z.string()).default([]),
    repoUrl: z.string().url().optional(),
    courseUrl: z.string().url().optional(),
    demoUrl: z.string().optional(),
    sourceDir: z.string().optional(),
    sourceFiles: z.array(z.string()).default([]),
    paid: z.boolean().default(false),
    price: z.string().optional(),
    buyUrl: z.string().url().optional(),
    featured: z.boolean().default(false),
    order: z.number().default(0),
  }),
});

const tokenTools = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/token-tools' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    description_en: z.string().optional(),
    repoUrl: z.string().url().optional(),
    demoUrl: z.string().url().optional(),
    tech: z.array(z.string()).default([]),
    featured: z.boolean().default(false),
    order: z.number().default(0),
  }),
});

const shorts = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/shorts' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    description_en: z.string().optional(),
    repoUrl: z.string().url().optional(),
    demoUrl: z.string().url().optional(),
    tech: z.array(z.string()).default([]),
    featured: z.boolean().default(false),
    order: z.number().default(0),
  }),
});

export const collections = { extensions, projects, courses, tokenTools, shorts };
