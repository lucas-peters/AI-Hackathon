import { fail, redirect } from "@sveltejs/kit";
export const actions = {
    default: async ({ request, cookies }) => {
        const data = await request.formData();
        console.log("Form Submitted!", data);
        let { name, password, confirm_password, email, location } =
            Object.fromEntries(data);
        if (password !== confirm_password) {
            return fail(422, { errors: "Passwords do not match" });
        }
        const response = await fetch(
            `${import.meta.env.VITE_API_URL}/create_account`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ name, password, email, location }),
            }
        );
        if (response.ok) {
            console.log("Response OK!");
            let jsonResponse = await response.json();
            let token = jsonResponse["access_token"];
            cookies.set("access_token", token, {
                path: "/",
                httpOnly: true,
                sameSite: "strict",
                maxAge: 60 * 60 * 24 * 1000,
            });
            return redirect(302, "/");
        } else {
            console.log("Fail!");
            return fail(422, { errors: "Invalid Credentials" });
        }
    },
};
