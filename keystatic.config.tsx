import { config, fields, collection } from '@keystatic/core';

export default config({
  storage: { kind: 'local' },

  ui: {
    brand: { name: 'Meii — content admin' },
  },

  collections: {
    courses: collection({
      label: 'Courses',
      slugField: 'title',
      path: 'src/content/courses/*',
      format: { contentField: 'content', data: 'yaml' },
      entryLayout: 'content',
      columns: ['title', 'paid', 'price', 'featured'],
      schema: {
        title: fields.slug({ name: { label: 'Title' } }),
        tagline: fields.text({ label: 'Tagline (optional)' }),
        description: fields.text({
          label: 'Description',
          multiline: true,
        }),
        thumbnail: fields.text({
          label: 'Thumbnail path',
          description: 'e.g. /courses/<slug>/thumbnail.png — drop the file in public/courses/<slug>/',
        }),
        video: fields.text({ label: 'Video path (optional)' }),
        videoFull: fields.text({ label: 'Full-length video path (optional)' }),
        duration: fields.text({ label: 'Duration (e.g. 0:45)' }),
        date: fields.date({ label: 'Date' }),
        tags: fields.array(fields.text({ label: 'Tag' }), {
          label: 'Tags',
          itemLabel: (props) => props.value,
        }),
        repoUrl: fields.url({ label: 'Repo URL (optional)' }),
        courseUrl: fields.url({ label: 'External course URL (optional)' }),
        demoUrl: fields.text({ label: 'Demo URL or path (optional)' }),
        sourceDir: fields.text({ label: 'Source dir (optional)' }),
        sourceFiles: fields.array(fields.text({ label: 'Source file' }), {
          label: 'Source files',
          itemLabel: (props) => props.value,
        }),
        paid: fields.checkbox({ label: 'Paid course', defaultValue: false }),
        price: fields.text({
          label: 'Price (display string, e.g. 299k or $29)',
        }),
        buyUrl: fields.url({ label: 'Buy URL (Gumroad / Stripe / Lemon Squeezy)' }),
        featured: fields.checkbox({ label: 'Featured', defaultValue: false }),
        order: fields.integer({ label: 'Order', defaultValue: 0 }),
        content: fields.text({
          label: 'Body (markdown)',
          multiline: true,
        }),
      },
    }),

    extensions: collection({
      label: 'Extensions',
      slugField: 'title',
      path: 'src/content/extensions/*',
      format: { data: 'yaml' },
      columns: ['title', 'platform', 'order'],
      schema: {
        title: fields.slug({ name: { label: 'Title' } }),
        description: fields.text({
          label: 'Description',
          multiline: true,
        }),
        platform: fields.select({
          label: 'Platform',
          options: [
            { label: 'VS Code', value: 'vscode' },
            { label: 'Chrome', value: 'chrome' },
            { label: 'Firefox', value: 'firefox' },
            { label: 'JetBrains', value: 'jetbrains' },
            { label: 'Raycast', value: 'raycast' },
            { label: 'Other', value: 'other' },
          ],
          defaultValue: 'vscode',
        }),
        demoUrl: fields.url({ label: 'Demo URL (optional)' }),
        installUrl: fields.url({ label: 'Install URL (optional)' }),
        repoUrl: fields.url({ label: 'Repo URL (optional)' }),
        installs: fields.integer({ label: 'Install count (optional)' }),
        order: fields.integer({ label: 'Order', defaultValue: 0 }),
      },
    }),

    projects: collection({
      label: 'Projects',
      slugField: 'title',
      path: 'src/content/projects/*',
      format: { data: 'yaml' },
      columns: ['title', 'featured', 'order'],
      schema: {
        title: fields.slug({ name: { label: 'Title' } }),
        description: fields.text({
          label: 'Description',
          multiline: true,
        }),
        repoUrl: fields.url({ label: 'Repo URL (optional)' }),
        demoUrl: fields.url({ label: 'Demo URL (optional)' }),
        tech: fields.array(fields.text({ label: 'Tech' }), {
          label: 'Tech stack',
          itemLabel: (props) => props.value,
        }),
        featured: fields.checkbox({ label: 'Featured', defaultValue: false }),
        order: fields.integer({ label: 'Order', defaultValue: 0 }),
      },
    }),

    tokenTools: collection({
      label: 'Token tools',
      slugField: 'title',
      path: 'src/content/token-tools/*',
      format: { data: 'yaml' },
      columns: ['title', 'featured', 'order'],
      schema: {
        title: fields.slug({ name: { label: 'Title' } }),
        description: fields.text({
          label: 'Description',
          multiline: true,
        }),
        repoUrl: fields.url({ label: 'Repo URL (optional)' }),
        demoUrl: fields.url({ label: 'Demo URL (optional)' }),
        tech: fields.array(fields.text({ label: 'Tech' }), {
          label: 'Tech stack',
          itemLabel: (props) => props.value,
        }),
        featured: fields.checkbox({ label: 'Featured', defaultValue: false }),
        order: fields.integer({ label: 'Order', defaultValue: 0 }),
      },
    }),

    shorts: collection({
      label: 'AI shorts',
      slugField: 'title',
      path: 'src/content/shorts/*',
      format: { data: 'yaml' },
      columns: ['title', 'featured', 'order'],
      schema: {
        title: fields.slug({ name: { label: 'Title' } }),
        description: fields.text({
          label: 'Description',
          multiline: true,
        }),
        repoUrl: fields.url({ label: 'Repo URL (optional)' }),
        demoUrl: fields.url({ label: 'Demo URL (optional)' }),
        tech: fields.array(fields.text({ label: 'Tech' }), {
          label: 'Tech stack',
          itemLabel: (props) => props.value,
        }),
        featured: fields.checkbox({ label: 'Featured', defaultValue: false }),
        order: fields.integer({ label: 'Order', defaultValue: 0 }),
      },
    }),
  },
});
