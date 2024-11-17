<script lang="ts">
    import "../app.css";
    import { Navbar } from "$lib/components/Navbar";
    import { Card } from "$lib/components/Card";
    import { Input } from "$lib/components/Input";
    import { Slider } from "$lib/components/Slider";
    import type { PageData } from "./$types";
    import { onMount } from "svelte";

    let { data }: { data: PageData } = $props();
    let isLoading = $state(false);
    let recommendations: any = $state([]);
    async function sendPrompt(prompt: string) {
        isLoading = true;
        let response = await fetch(`/api`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, DELETE, PUT, GET",
                "Access-Control-Allow-Headers":
                    "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With",
                "Cross-Domain": "true",
            },
            body: JSON.stringify({ prompt, email: data.context.user.email }),
        });
        let jsonResponse = await response.json();
        console.log(jsonResponse);
        // recommendations = jsonResponse.products;
        isLoading = false;
    }

    console.log(data);
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
            <Card
                width={250}
                height={250}
                image={isLoading ? "" : data.context.outfit.top.filename}
            />
            <Card
                width={250}
                height={250}
                image={isLoading ? "" : data.context.outfit.bottom.filename}
            />
            <Card
                width={250}
                height={250}
                image={isLoading ? "" : data.context.outfit.footwear.filename}
            />
        </div>
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
    <div
        class="fixed bottom-0 w-full flex justify-center items-center bg-violet-50 py-4"
    >
        <Input
            onClick={sendPrompt}
            {isLoading}
            withCTA
            class="w-full rounded-md border-0 py-2.5 pl-7 pr-24 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-violet-400 sm:text-sm/6"
            placeholder="What's the occassion"
        />
    </div>
</div>
