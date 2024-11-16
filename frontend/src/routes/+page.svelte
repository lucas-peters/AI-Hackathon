<script lang="ts">
    import '../app.css'
    import { Navbar } from '$lib/components/Navbar'
    import { Card } from '$lib/components/Card'
    import { Input } from '$lib/components/Input'
    let image: string = "https://placehold.co/300";
    let c = "w-full"
</script>
<Navbar />
<div class="w-full flex justify-center items-center my-16">
    <h1 class="text-4xl">Welcome to Your Outfit of the Day!</h1>
</div>
<div class="container mx-auto flex flex-col justify-center items-center">
    <div class="flex gap-3 justify-center mb-10">
        <Card {image} title="Shirt"/>
        <Card {image} title="Pants"/>
        <Card {image} title="Shoes"/>
    </div>
    <div class="fixed bottom-0 w-full flex justify-center items-center bg-violet-50 py-4">
        <Input/>
    </div>
</div>