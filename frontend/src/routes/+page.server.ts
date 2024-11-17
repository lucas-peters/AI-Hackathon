import { redirect, error } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";
import jwt from "jsonwebtoken";

export const load: PageServerLoad = async ({ cookies }) => {
    let access_token = cookies.get("access_token");
    if (access_token) {
        try {
            console.log("Access token found!");
            let decoded = jwt.verify(
                access_token,
                import.meta.env.VITE_JWT_SECRET
            );
            console.log(decoded);
            const requestBody = {
                prompt: "",
                email: (decoded as jwt.JwtPayload).sub,
            };
            const response = await fetch(`${import.meta.env.VITE_API_URL}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(requestBody),
            });
            if (!response.ok) {
                console.log("Response not OK!");
                return error(response.status);
            }
            let jsonResponse = await response.json();
            console.log("Response:", jsonResponse);
            return {
                status: 200,
                context: {
                    user: { access_token },
                },
            };
        } catch (error) {
            console.log("JWT Error:", error);
            cookies.delete("access_token", { path: "/" });
            return redirect(307, "/login");
        }
    } else {
        console.log("Access token not found!");
        throw redirect(307, "/login");
    }
};
