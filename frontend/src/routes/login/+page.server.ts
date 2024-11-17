import { fail, redirect } from "@sveltejs/kit";

export const actions = {
    default: async ({ request, cookies }) => {
        const data = await request.formData();
        let { email, password } = Object.fromEntries(data);
        const response = await fetch(`${import.meta.env.VITE_API_URL}/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email, password }),
            credentials: "include",
        });
        if (response.ok) {
            console.log("Response OK!");
            let token = await response.json();
            cookies.set("access_token", token, {
                path: "/",
                httpOnly: true,
                sameSite: "strict",
                maxAge: 60 * 60 * 24 * 1000,
            });
            throw redirect(302, "/");
        } else {
            console.log("Fail!");
            console.log(response);
            return fail(422, { errors: "Invalid Credentials" });
        }
    },
};
