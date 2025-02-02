<script>
  import { onMount } from "svelte";
  import { writable } from 'svelte/store';
  
  // Makes it so that if there is an item in local storage to set the 
  // visits to that otherwise to set it to 0
  const initialVisits = typeof localStorage !== 'undefined' ?
    parseInt(localStorage.getItem('visits')) || 0 : 
    0;
  let visits = writable(initialVisits);


  onMount(() => {
    // Check if visitor has already been counted in this session
    if (!sessionStorage.getItem("visited")) {
      fetch("http://127.0.0.1:5173")  // Replace with AWS API Gateway URL
        .then((response) => response.json())
        .then((data) => {$visits = data.visits; localStorage.setItem("visits", data.visits)})
        .catch((error) => console.error("Error updating visitor count:", error));

      // Mark as visited in sessionStorage
      sessionStorage.setItem("visited", "true");
    }
  });
</script>


<div class="h-screen flex flex-col items-center justify-center">
  <h1 class="mb-20 font-honk text-8xl">Kareem Eldahshoury</h1>
            <div class="mt-5">
              <a href="/experiences" class="mr-10 font-semibold text-yellow-neon bg-pink-neon rounded-lg p-2.5 border border-4 border-black">Experiences</a>
              <a href="/projects" class="mr-10 font-semibold text-yellow-neon bg-pink-neon rounded-lg p-2.5 border border-4 border-black">Projects</a>
              <a href="/full" class="mr-10 font-semibold text-yellow-neon bg-pink-neon rounded-lg p-2.5 border border-4 border-black">Full Resume</a>
              <a href="/about" class="mr-10 font-semibold text-yellow-neon bg-pink-neon rounded-lg p-2.5 border border-4 border-black">About</a>
          </div>
          
          <div class="mt-20">
            <!-- {#if visits}
            <h1> Visitor Count: {visits}</h1>
            {:else}
            <h1> Visitor Count: {actual_visits}</h1>
            {/if} -->
            <h1> Visitor Count: {$visits}</h1>
          </div>
</div>
