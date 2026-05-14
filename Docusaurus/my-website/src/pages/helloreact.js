import ExecutionEnvironment from '@docusaurus/ExecutionEnvironment';

// This code runs when the site first loads in the browser
if (ExecutionEnvironment.canUseDOM) {
  console.log('Docusaurus site has loaded!');
  // Add global event listeners or analytics here
}

export function onRouteDidUpdate({location, previousLocation}) {
  // This runs every time the user navigates to a new page
  if (location.pathname !== previousLocation?.pathname) {
    console.log(`Navigated to: ${location.pathname}`);
    // Re-initialize scripts that need to run on every page (like ads or trackers)
  }
}
