<script lang="ts">
    import { Input } from "$lib/components/Input";
    import { onMount } from "svelte";

    let getPosition = $state(false);
    let coords: any = $state(null);
    let Geolocation: any = $state(null);
    let geoLoading = $state(false);
    let geoSuccess = $state(false);
    let geoError: any = $state(null);
    let onMountReady = $state(false);

    let { form } = $props();

    onMount(async () => {
        Geolocation = (await import("svelte-geolocation")).default;
        onMountReady = true;
    });
</script>

<div class="w-screen h-screen flex justify-center items-center gradient">
    <div class="container mx-auto flex flex-col justify-center items-center">
        <div
            class="w-2/5 flex flex-col justify-center items-center border-violet-900 border-2 rounded py-12 bg-white"
        >
            <h1 class="text-4xl mb-4 w-full text-center">Register</h1>
            {#if form?.errors}
                <div
                    class="w-3/4 bg-red-500 text-white text-center rounded py-2 mt-4 mb-4"
                >
                    {form?.errors}
                </div>
            {/if}
            <form class="w-full flex flex-col items-center" method="POST">
                <Input
                    name="name"
                    type="text"
                    placeholder="Name"
                    class="w-full mb-2 rounded"
                    required
                />
                <Input
                    name="email"
                    type="email"
                    placeholder="Email"
                    class="w-full mb-2 rounded"
                    required
                />
                <Input
                    name="password"
                    type="password"
                    placeholder="Password"
                    class="w-full mb-2 rounded"
                    minlength={6}
                    required
                />
                <Input
                    name="confirm_password"
                    type="password"
                    placeholder="Confirm Password"
                    class="w-full mb-2 rounded"
                    minlength={6}
                    required
                />
                <div class="container flex w-3/4 justify-between items-center">
                    <div class="flex justify-center items-center">
                        <input
                            type="radio"
                            name="gender"
                            id="male"
                            value="male"
                            required
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
                            id="other"
                            value="other"
                        />
                        <label for="other" class="ml-3">Other</label>
                    </div>
                </div>
                <div
                    class="w-3/4 bg-violet-800 text-white text-center rounded py-2 mt-4"
                    onclick={(e) => {
                        console.log("Detect Location!");
                        e.preventDefault();
                        getPosition = true;
                    }}
                    role="button"
                    tabindex="0"
                    onkeydown={(e) => {
                        if (e.key === "Enter") {
                            getPosition = true;
                        }
                    }}
                >
                    {#if geoLoading}
                        Detecting Location...
                    {:else if geoSuccess}
                        Location Detected
                    {:else}
                        Detect Location
                    {/if}
                </div>
                <input
                    class="hidden"
                    type="text"
                    name="location"
                    value={coords}
                />
                {#if onMountReady}
                    <Geolocation
                        {getPosition}
                        bind:coords
                        bind:loading={geoLoading}
                        bind:success={geoSuccess}
                        bind:error={geoError}
                        let:notSupported
                    >
                        {#if notSupported}
                            Your browser does not support the Geolocation API.
                        {/if}
                    </Geolocation>
                {/if}
                <button
                    class="w-3/4 bg-violet-800 text-white rounded py-2 mt-4"
                    type="submit">Register</button
                >
            </form>
            <div class="w-full text-center mt-4">
                <h3 class="text-xl">-OR-</h3>
            </div>
            <a
                href="/login"
                class="w-3/4 bg-violet-800 text-white rounded py-2 mt-4 p-4 text-center"
                >Login</a
            >
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

    input[type="radio"]:after {
        width: 17px;
        height: 17px;
        border-radius: 15px;
        top: -2px;
        left: -1px;
        position: relative;
        background-color: #d1d3d1;
        content: "";
        display: inline-block;
        visibility: visible;
        border: 2px solid white;
    }

    input[type="radio"]:checked:after {
        width: 17px;
        height: 17px;
        border-radius: 15px;
        top: -2px;
        left: -1px;
        position: relative;
        background-color: #3730a3;
        content: "";
        display: inline-block;
        visibility: visible;
        border: 2px solid white;
    }
</style>
