<script lang="ts">
    import '../app.css'
    import { Navbar } from '$lib/components/Navbar'
    import { Card } from '$lib/components/Card'
    let image: string = "https://placehold.co/300";
</script>
<Navbar />
<div class="w-full flex justify-center items-center my-16">
    <h1 class="text-4xl">Welcome to Your Outfit of the Day!</h1>
</div>
<div class="container mx-auto flex gap-3 justify-center">
    <Card {image} title="Shirt"/>
    <Card {image} title="Pants"/>
    <Card {image} title="Shoes"/>
</div>