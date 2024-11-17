<script lang="ts">
    import { onMount } from "svelte";
    import { register } from "swiper/element/bundle";
    import { Card } from "$lib/components/Card";
    import Swiper from "swiper/bundle";

    register();
    let swiperEl: any = null;
    let swiperObj: any = null;

    function prev() {
        if (swiperEl && !swiperObj) {
            swiperObj = swiperEl.swiper;
        }
        swiperObj.slidePrev();
    }

    function next() {
        if (swiperEl && !swiperObj) {
            swiperObj = swiperEl.swiper;
        }
        console.log(swiperObj);
        swiperObj.slideNext();
    }
</script>

<div class="flex items-center">
    <button onclick={prev} class="h-full" aria-label="Previous">
        <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="#5b21b6"
            class="size-6"
        >
            <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M15.75 19.5 8.25 12l7.5-7.5"
            />
        </svg>
    </button>
    <swiper-container
        bind:this={swiperEl}
        class="-z-10 mt-4 mb-10 max-w-[95%]"
        space-between="30"
        observer={true}
        loop={true}
    >
        {#each { length: 10 } as _, i}
            <swiper-slide key={i} class="!w-auto">
                <Card
                    image="https://picsum.photos/200"
                    title="Lorem Ipsum"
                    body="$20.00"
                />
            </swiper-slide>
        {/each}
    </swiper-container>
    <button onclick={next} class="h-full" aria-label="Next"
        ><svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="#5b21b6"
            class="size-6"
        >
            <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="m8.25 4.5 7.5 7.5-7.5 7.5"
            />
        </svg>
    </button>
</div>
