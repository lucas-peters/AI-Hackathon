import { redirect } from "@sveltejs/kit";
import type { Handle } from "@sveltejs/kit";

export const handle: Handle = async ({ event, resolve }) => {
    const { cookies } = event;
    const access_token = cookies.get("access_token");

    if (access_token) {
        return await resolve(event);
    }
    return await redirect(403, "/login");
};
