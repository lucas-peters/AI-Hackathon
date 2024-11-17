<script lang="ts">
    import "../app.css";
    import { Navbar } from "$lib/components/Navbar";
    import { Card } from "$lib/components/Card";
    import { Input } from "$lib/components/Input";
    import { Slider } from "$lib/components/Slider";
    import type { PageData } from "./$types";
    import { onMount } from "svelte";

    let { data }: { data: PageData } = $props();
    let formElement: HTMLFormElement;
    let recommendations: any = $state([]);
    let updateOutfitKey: number = $state(0);
    console.log("Page Data", data.context.outfit);
    let coords: any = $state(null);
    let datetime: Date = new Date();
    function submitForm() {
        return Promise.resolve(formElement.submit());
    }
    onMount(() => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition((position) => {
                coords = position.coords;
            });
        }
    });
</script>

<div class="mb-[100px]">
    <Navbar />
    <div class="w-full flex justify-center items-center mt-8">
        <h1 class="text-4xl">Welcome to Your Outfit of the Day!</h1>
    </div>
    <!-- Outfit of the day Section -->
    <div
        class="container mx-auto flex flex-col justify-center items-center mt-8"
    >
        <div class="flex gap-3 justify-center mb-10">
            {#key updateOutfitKey}
                {#if data.context?.outfit.top?.filename}
                    <Card
                        width={250}
                        height={250}
                        image={data.context?.outfit.top?.filename}
                    />
                {/if}
                {#if data.context?.outfit.bottom?.filename}
                    <Card
                        width={250}
                        height={250}
                        image={data.context?.outfit.bottom?.filename}
                    />
                {/if}
                {#if data.context?.outfit.footwear?.filename}
                    <Card
                        width={250}
                        height={250}
                        image={data.context?.outfit.footwear?.filename}
                    />
                {/if}
            {/key}
        </div>
        {#if !data.context?.outfit.footwear?.filename || !data.context?.outfit.bottom?.filename || !data.context?.outfit.top?.filename}
            <p class="text-lg text-gray-500">You need to buy more clothes</p>
        {/if}
    </div>
    <!-- Recommendation Section -->
    {#if recommendations.length > 0}
        <div class="container mx-auto">
            <h3 class="text-2xl">Explore more</h3>
        </div>
        <div class="w-screen mt-4 px-10">
            <Slider data={recommendations} />
        </div>
    {/if}
    <!-- Prompt Section -->
    <form
        bind:this={formElement}
        class="fixed bottom-0 w-full flex justify-center items-center bg-violet-50 py-4"
        method="POST"
        onsubmit={async (e) => {
            e.preventDefault();
            await submitForm();
            updateOutfitKey++;
        }}
    >
        <Input
            name="prompt"
            withCTA
            class="w-full rounded-md border-0 py-2.5 pl-7 pr-24 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-violet-400 sm:text-sm/6"
            placeholder="What's the occassion"
        />
        <input class="hidden" type="text" name="location" value={coords} />
        <input class="hidden" type="text" name="location" value={datetime} />
    </form>
</div>
