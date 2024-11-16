<script lang="ts">
    export let image: string = "";
    export let title: string = "";
    export let body: string = "";
</script>

<div class="max-w-sm rounded overflow-hidden shadow-lg">
    <img src={image} alt="{title} Image" class="w-full" />
    <div class="px-4 py-4">
        <div class="font-bold text-xl mb-2">{title}</div>
        {#if body}
            <p class="text-gray-700 text-base">{body}</p>
        {/if}
    </div>
</div>
