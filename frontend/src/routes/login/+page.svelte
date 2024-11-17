<script lang="ts">
    import { Input } from "$lib/components/Input";
    import { onMount } from "svelte";
    let formEl: HTMLFormElement;
    onMount(() => {
        formEl.addEventListener("submit", (e) => {
            e.preventDefault();
            const formData = new FormData(formEl);
            const data = Object.fromEntries(formData.entries());
            console.log(data);
        });
    });
</script>

<div class="w-screen h-screen flex justify-center items-center gradient">
    <div class="container mx-auto flex flex-col justify-center items-center">
        <div
            class="w-2/5 flex flex-col justify-center items-center border-violet-900 border-2 rounded py-12 bg-white"
        >
            <h1 class="text-4xl mb-4 w-full text-center">Login</h1>
            <form class="w-full flex flex-col items-center" bind:this={formEl}>
                <Input
                    name="email"
                    type="email"
                    placeholder="Email"
                    class="w-full mb-2 rounded"
                />
                <Input
                    name="password"
                    type="password"
                    placeholder="Password"
                    class="w-full rounded"
                />
                <button
                    class="w-3/4 bg-violet-800 text-white rounded py-2 mt-4"
                    type="submit">Login</button
                >
            </form>
        </div>
    </div>
</div>

<style>
    .gradient {
        background: linear-gradient(
            50deg,
            rgba(245, 243, 255, 1) 0%,
            rgba(91, 33, 182, 1) 35%
        );
    }
</style>
