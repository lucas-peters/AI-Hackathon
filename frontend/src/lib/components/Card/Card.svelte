<script lang="ts">
    export let image: string = "";
    export let title: string = "";
</script>
<div class="max-w-sm rounded overflow-hidden shadow-lg">
    <img src={image} alt="{title} Image" class="w-full">
    <div class="px-4 py-4">
        <div class="font-bold text-xl mb-2">{title}</div>
    </div>
</div>