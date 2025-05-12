// src/views/AboutView.versions.js
// Version history for AboutView.vue (Nexomon Extinction Database)

export default [
  { 
    version: '1.4.0',
    date: 'May 12, 2025',
    changes: [
      'Added Skill Tree section to NexomonDetails',
      'Added Skill Database',
    ]
  },
  {
    version: '1.3.0',
    date: 'May 10, 2025',
    changes: [
      'Consistent button and card styling across all components',
      'Smart navigation and contextual back button in NexomonDetails',
      '"View Region Details" button in NexomonDetails',
      'Improved NexomonList and LocationDetails card design, responsive images, and number display',
      'LocationDetails: Nexomon with location exceptions are visually marked and show tooltips',
      'Map selection is persisted per region in localStorage and restored when returning from NexomonDetails',
      'Location search bar now matches both region names and subarea/map names',
    ]
  },
  {
    version: '1.2.0',
    date: 'May 2, 2025',
    changes: [
      'Added About page with project information',
      'Fixed dark mode issues',
      "Added 'Element' filter",
      'Overall improvements to UI and functionality'
    ]
  },
  {
    version: '1.1.0',
    date: 'October 15, 2024',
    changes: [
      'More bug fixes',
      'Improved Battle Info section',
      'Updated page titles'
    ]
  },
  {
    version: '1.0.2',
    date: 'October 13, 2024',
    changes: [
      'Improved maps functionality',
      'Enhanced responsive design for mobile devices',
      'Added Nexomon descriptions',
      'Fixed various bugs'
    ]
  },
  {
    version: '1.0.1',
    date: 'October 12, 2024',
    changes: [
      'Implemented image preloading for better performance',
      'Visual improvements',
      'Enhanced food and battle info sections'
    ]
  },
  {
    version: '1.0.0',
    date: 'October 9, 2024',
    changes: [
      'Initial release',
      'Added dark mode toggle',
      'Implemented map hover and zoom functionality',
      'Fixed location display for all Nexomon',
      'Enhanced responsive design',
      'Added region containers with interactive maps'
    ]
  }
];
