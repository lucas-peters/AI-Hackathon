import { redirect } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ cookies }) => {
    let access_token = cookies.get("access_token");
    if (access_token) {
        console.log("Access token found!");

        return {
            status: 200,
            context: {
                user: { access_token },
            },
        };
    } else {
        console.log("Access token not found!");
        // throw redirect(307, "/login");
    }
};
