<!-- <script context="module">
  // Disable pre-rendering so the API call runs on the client
  export const prerender = false;
</script>

<script>
  import { onMount } from "svelte";
  import { writable } from "svelte/store";

  // Initialize the visitor count from localStorage (if available)
  const initialVisits =
    typeof localStorage !== "undefined"
      ? parseInt(localStorage.getItem("visits")) || 0
      : 0;
  let visits = writable(initialVisits);
  //let pageRefreshed = writable(false);

  onMount(() => {
    const pageLoaded = sessionStorage.getItem("pageLoaded");

    if (!pageLoaded) {
      sessionStorage.setItem("pageLoaded", "true");
      //pageRefreshed.set(true);

      // Fetch from the API to update the visitor count
      fetch("/api", { cache: "no-store" })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          return response.json();
        })
        .then((data) => {
          console.log("Visitor Count Response:", data);
          // Assuming your data returns an object with an Item key that contains count
          visits.set(data.Item.count);
          localStorage.setItem("visits", data.Item.count);
        })
        .catch((error) =>
          console.error("Error updating visitor count:", error)
        );
    } else {
      console.log("Page already loaded in this tab; skipping API call.");
    }
  });
</script> -->

<div class="min-h-screen flex flex-col items-center justify-center p-4">
  <h1 class="mb-8 sm:mb-12 md:mb-16 lg:mb-20 font-dm-mono text-light-purple text-4xl sm:text-5xl md:text-6xl lg:text-7xl xl:text-8xl text-center">
    Kareem Eldahshoury
  </h1>
  
  <div class="mt-5 flex flex-col sm:flex-row gap-4 sm:gap-0 items-center justify-center w-full max-w-4xl px-4">
    <a
      href="/experiences"
      class="w-full sm:w-auto sm:mr-4 md:mr-6 lg:mr-10 font-dm-mono font-semibold text-darkest-purple bg-lightest-purple rounded-lg p-2.5 border border-4 border-darkest-purple text-center hover:scale-105 transition-transform hover:text-lightest-purple hover:bg-darkest-purple"
      >Experiences</a
    >
    <a
      href="/projects"
      class="w-full sm:w-auto sm:mr-4 md:mr-6 lg:mr-10 font-dm-mono font-semibold text-darkest-purple bg-lightest-purple rounded-lg p-2.5 border border-4 border-darkest-purple text-center hover:scale-105 transition-transform hover:text-lightest-purple hover:bg-darkest-purple"
      >Projects</a
    >
    <a
      href="/full"
      class="w-full sm:w-auto sm:mr-4 md:mr-6 lg:mr-10 font-dm-mono font-semibold text-darkest-purple bg-lightest-purple rounded-lg p-2.5 border border-4 border-darkest-purple text-center hover:scale-105 transition-transform hover:text-lightest-purple hover:bg-darkest-purple"
      >Full Resume</a
    >
    <a
      href="/about"
      class="w-full sm:w-auto font-dm-mono font-semibold text-darkest-purple bg-lightest-purple rounded-lg p-2.5 border border-4 border-darkest-purple text-center hover:scale-105 transition-transform hover:text-lightest-purple hover:bg-darkest-purple"
      >About</a
    >
  </div>

  <!-- <div class="mt-12 sm:mt-16 md:mt-20">
    <h1 class="text-center text-sm sm:text-base"> Visitor Count: {$visits} </h1>
  </div> -->
</div>