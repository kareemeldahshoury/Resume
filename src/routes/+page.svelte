<script context="module">
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
</script>

<div class="h-screen flex flex-col items-center justify-center">
  <h1 class="mb-20 font-honk text-8xl">Kareem Eldahshoury</h1>
  <div class="mt-5">
    <a
      href="/experiences"
      class="mr-10 font-semibold text-yellow-neon bg-pink-neon rounded-lg p-2.5 border border-4 border-black"
      >Experiences</a
    >
    <a
      href="/projects"
      class="mr-10 font-semibold text-yellow-neon bg-pink-neon rounded-lg p-2.5 border border-4 border-black"
      >Projects</a
    >
    <a
      href="/full"
      class="mr-10 font-semibold text-yellow-neon bg-pink-neon rounded-lg p-2.5 border border-4 border-black"
      >Full Resume</a
    >
    <a
      href="/about"
      class="mr-10 font-semibold text-yellow-neon bg-pink-neon rounded-lg p-2.5 border border-4 border-black"
      >About</a
    >
  </div>

  <div class="mt-20">
    <h1> Visitor Count: {$visits} </h1>
  </div>
</div>
