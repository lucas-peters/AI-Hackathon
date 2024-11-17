<script lang="ts">
    import { Input } from "$lib/components/Input";
    let { form } = $props();
</script>

<div class="w-screen h-screen flex justify-center items-center gradient">
    <div class="container mx-auto flex flex-col justify-center items-center">
        <div
            class="w-2/5 flex flex-col justify-center items-center border-violet-900 border-2 rounded py-12 bg-white"
        >
            <h1 class="text-4xl mb-4 w-full text-center">Login</h1>
            {#if form?.errors}
                <div
                    class="w-3/4 bg-red-500 text-white text-center rounded py-2 mt-4 mb-4"
                >
                    {form?.errors}
                </div>
            {/if}
            <form class="w-full flex flex-col items-center" method="POST">
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
            <div class="w-full text-center"><h3 class="text-xl">-OR-</h3></div>
            <a href="/register" class="underline text-violet-800">Register</a>
        </div>
    </div>
</div>
