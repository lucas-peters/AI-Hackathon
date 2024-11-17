<script lang="ts">
    import "../app.css";
    import { Navbar } from "$lib/components/Navbar";
    import { Card } from "$lib/components/Card";
    import { Input } from "$lib/components/Input";
    import { Slider } from "$lib/components/Slider";

    let image: string = "https://picsum.photos/300";
    let isLoading = $state(false);
    let recommendations: any = $state([]);
    async function sendPrompt(prompt: string) {
        isLoading = true;
        let response = await fetch("https://dummyjson.com/products?count=10", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        });
        let jsonResponse = await response.json();
        recommendations = jsonResponse.products;
        isLoading = false;
    }
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
            <Card width={250} height={250} image={isLoading ? "" : image} />
            <Card width={250} height={250} image={isLoading ? "" : image} />
            <Card width={250} height={250} image={isLoading ? "" : image} />
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
