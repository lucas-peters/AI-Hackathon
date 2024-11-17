<script lang="ts">
    let isOpen = false;
    function toggleMenu() {
        isOpen = !isOpen;
    }

    function signout() {
        document.cookie =
            "username=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
        window.location.replace(`${window.location.origin}/login`);
    }
</script>

<nav class="bg-violet-800">
    <div class="mx-auto px-2 sm:px-6 lg:px-8">
        <div class="relative flex h-16 items-center justify-between">
            <div
                class="flex flex-1 items-center justify-center sm:items-stretch sm:justify-start"
            >
                <div class="flex shrink-0 items-center">
                    <img
                        class="h-8 w-auto"
                        src="https://img.logoipsum.com/292.svg"
                        alt="Your Company"
                    />
                </div>
                <div class="w-full">
                    <h3 class="text-4xl text-white text-center">Doojoo</h3>
                </div>
            </div>
            <div
                class="absolute inset-y-0 right-0 flex items-center pr-2 sm:static sm:inset-auto sm:ml-6 sm:pr-0"
            >
                <div class="relative ml-3">
                    <div
                        role="button"
                        tabindex="0"
                        onclick={toggleMenu}
                        onkeydown={(e) => e.key === "Enter" && toggleMenu()}
                        onkeyup={(e) => e.key === "Enter" && toggleMenu()}
                        aria-roledescription="button"
                    >
                        <img
                            class="size-8 rounded-full"
                            src="https://i.pravatar.cc/300"
                            alt=""
                        />
                    </div>
                    {#if isOpen}
                        <div
                            class="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 ring-black/5 focus:outline-none"
                            role="menu"
                            aria-orientation="vertical"
                            aria-labelledby="user-menu-button"
                            tabindex="-1"
                        >
                            <a
                                href="#"
                                class="block px-4 py-2 text-sm text-gray-700"
                                role="menuitem"
                                tabindex="-1"
                                id="user-menu-item"
                                onclick={signout}>Sign out</a
                            >
                        </div>
                    {/if}
                </div>
            </div>
        </div>
    </div>
</nav>
