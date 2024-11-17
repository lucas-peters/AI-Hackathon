<script lang="ts">
    let {
        image = "",
        title = "",
        body = "",
        width = 250,
        height = 250,
        class: className = "",
        imgClass = "",
        onClick = () => {},
        role = "card",
    } = $props();
</script>

<div
    class="max-w-sm rounded overflow-hidden shadow-lg {role == 'card'
        ? 'cursor-pointer'
        : ''} {className}"
    tabindex="-1"
    onclick={() => onClick()}
    onkeydown={(e) => {
        if (e.key === "Enter") {
            onClick();
        }
    }}
    onkeyup={(e) => {
        if (e.key === "Enter") {
            onClick();
        }
    }}
    aria-roledescription={role}
    {role}
>
    <div style="width: {width}px; height: {height}px;">
        {#if image}
            <img
                src={image}
                alt="{title} Image"
                class="w-full h-full {imgClass}"
            />
        {:else}
            <div class="w-full h-full animated-loader"></div>
        {/if}
    </div>
    {#if title || body}
        <div class="px-4 py-4">
            <div class="font-bold text-xl mb-2">{title}</div>
            {#if body}
                <p class="text-gray-700 text-base">{body}</p>
            {/if}
        </div>
    {/if}
</div>

<style>
    .animated-loader {
        animation-duration: 1s;
        animation-fill-mode: forwards;
        animation-iteration-count: infinite;
        animation-name: gradientLoader;
        animation-timing-function: linear;
        background: #f6f7f8;
        background: linear-gradient(
            to right,
            #eeeeee 8%,
            #dddddd 18%,
            #eeeeee 33%
        );
        background-size: 800px 104px;
        position: relative;
    }
</style>
