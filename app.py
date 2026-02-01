// Setup type definitions for built-in Supabase Runtime APIs
import "jsr:@supabase/functions-js/edge-runtime.d.ts";

Deno.serve(async (req) => {
    // 🔐 Webhook secret validation
    const authHeader = req.headers.get("authorization");
    const secret = Deno.env.get("WEBHOOK_SECRET");

    if (authHeader !== `Bearer ${secret}`) {
        return new Response("Unauthorized", { status: 401 });
    }

    // Your function logic here
    const message = `Hello`;
    return new Response(message, {
        headers: { "Content-Type": "text/plain" },
    });
});
