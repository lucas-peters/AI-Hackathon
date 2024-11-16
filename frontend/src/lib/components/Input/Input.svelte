<script lang="ts">
    import { Loader } from "$lib/components/Loader";

    let prompt = $state("");
    let { onClick, isLoading } = $props();

    function handleClick() {
        onClick(prompt);
        prompt = "";
    }
</script>

<div class="relative w-3/4">
    <input
        bind:value={prompt}
        type="text"
        placeholder="Where are you going?"
        class="w-full rounded-md border-0 py-2.5 pl-7 pr-24 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-violet-400 sm:text-sm/6"
    />
    <button
        class="absolute inset-y-0 right-0 flex items-center justify-center w-20 bg-violet-800 rounded-md text-white text-sm/6 font-semibold"
        aria-label="Send"
        onclick={handleClick}
    >
        {#if isLoading}
            <Loader />
        {:else}
            <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                stroke="currentColor"
                class="size-6"
            >
                <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M6 12 3.269 3.125A59.769 59.769 0 0 1 21.485 12 59.768 59.768 0 0 1 3.27 20.875L5.999 12Zm0 0h7.5"
                />
            </svg>
        {/if}
    </button>
</div>
