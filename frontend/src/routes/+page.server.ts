import { redirect, error } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";
import jwt from "jsonwebtoken";
import { page } from "$app/stores";
let pageLoaded = false;
let responseBody: any;
export const load: PageServerLoad = async (/*{ cookies }*/) => {
    if (pageLoaded) {
        return responseBody;
    }
    console.log("Loading Page!");
    // let access_token = cookies.get("access_token");
    // if (access_token) {
    // try {
    // let decoded = jwt.verify(
    //     access_token,
    //     import.meta.env.VITE_JWT_SECRET
    // );
    // console.log(decoded);
    const requestBody = {
        prompt: "",
        email: "lucas@gmail.com",
    };
    const response = await fetch(`${import.meta.env.VITE_API_URL}/recommend`, {
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
    pageLoaded = true;
    responseBody = {
        status: 200,
        context: {
            user: {
                // access_token,
                email: "lucas@gmail.com",
            },
            outfit: jsonResponse.body,
        },
    };
    return responseBody;
    // } catch (error) {
    //     console.log("JWT Error:", error);
    //     cookies.delete("access_token", { path: "/" });
    //     return redirect(307, "/login");
    // }
    // } else {
    //     console.log("Access token not found!");
    //     throw redirect(307, "/login");
    // }
};
export const actions = {
    default: async ({ request }) => {
        let data = await request.formData();
        let { prompt, datetime, coords } = Object.fromEntries(data);
        console.log("Default Action!", data);
        // let access_token = cookies.get("access_token");
        // if (access_token) {
        // try {
        // console.log("Access token found!");
        // let decoded = jwt.verify(
        //     access_token,
        //     import.meta.env.VITE_JWT_SECRET
        // );
        // console.log(decoded);
        const requestBody = {
            prompt: prompt,
            datetime: datetime,
            location: coords,
            email: "lucas@gmail.com",
        };
        console.log(requestBody);
        const response = await fetch(
            `${import.meta.env.VITE_API_URL}/recommend`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(requestBody),
            }
        );
        if (!response.ok) {
            console.log("Response not OK!");
            return error(response.status);
        }
        let jsonResponse = await response.json();
        console.log("JR", jsonResponse);
        responseBody = {
            status: 200,
            context: {
                user: {
                    // access_token,
                    email: "lucas@gmail.com",
                },
                outfit: jsonResponse.body,
            },
        };
        return responseBody;
        // } catch (error) {
        //     console.log("JWT Error:", error);
        //     cookies.delete("access_token", { path: "/" });
        //     // return redirect(307, "/login");
        // }
        // } else {
        //     console.log("Access token not found!");
        //     // throw redirect(307, "/login");
        // }
    },
};
