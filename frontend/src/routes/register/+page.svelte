<script lang="ts">
    import { Input } from "$lib/components/Input";
    import { onMount } from "svelte";

    let getPosition = false;
    let Geolocation: any;
    let onMountReady = false;
    let formEl: HTMLFormElement;

    onMount(async () => {
        Geolocation = (await import("svelte-geolocation")).default;
        formEl.addEventListener("submit", (e) => {
            e.preventDefault();
            const formData = new FormData(formEl);
            const data = Object.fromEntries(formData.entries());
            console.log(data);
        });
        onMountReady = true;
    });
</script>

<div class="w-screen h-screen flex justify-center items-center gradient">
    <div class="container mx-auto flex flex-col justify-center items-center">
        <div
            class="w-2/5 flex flex-col justify-center items-center border-violet-900 border-2 rounded py-12 bg-white"
        >
            <h1 class="text-4xl mb-4 w-full text-center">Register</h1>
            <form class="w-full flex flex-col items-center" bind:this={formEl}>
                <Input
                    name="name"
                    type="text"
                    placeholder="Name"
                    class="w-full mb-2 rounded"
                />
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
                    class="w-full mb-2 rounded"
                />
                <Input
                    name="confirm_password"
                    type="password"
                    placeholder="Confirm Password"
                    class="w-full mb-2 rounded"
                />
                <div class="container flex w-3/4 justify-between items-center">
                    <div class="flex justify-center items-center">
                        <input
                            type="radio"
                            name="gender"
                            id="male"
                            value="male"
                        />
                        <label for="male" class="ml-3">Male</label>
                    </div>
                    <div class="flex justify-center items-center">
                        <input
                            type="radio"
                            name="gender"
                            id="female"
                            value="female"
                        />
                        <label for="male" class="ml-3">Female</label>
                    </div>
                    <div class="flex justify-center items-center">
                        <input
                            type="radio"
                            name="gender"
                            id="prefer_not_to_say"
                            value="prefer_not_to_say"
                        />
                        <label for="prefer_not_to_say" class="ml-3"
                            >Prefer not to say</label
                        >
                    </div>
                </div>
                <button
                    class="w-3/4 bg-violet-800 text-white rounded py-2 mt-4"
                    onclick={() => (getPosition = true)}
                >
                    Detect Location
                </button>
                {#if onMountReady}
                    <Geolocation
                        {getPosition}
                        let:coords
                        let:loading
                        let:success
                        let:error
                        let:notSupported
                    >
                        {#if notSupported}
                            Your browser does not support the Geolocation API.
                        {:else}
                            {#if loading}
                                Loading...
                            {/if}
                            {#if success}
                                {JSON.stringify(coords)}
                            {/if}
                            {#if error}
                                An error occurred. {error.code} {error.message}
                            {/if}
                        {/if}
                    </Geolocation>
                {/if}
                <button
                    class="w-3/4 bg-violet-800 text-white rounded py-2 mt-4"
                    type="submit">Register</button
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
