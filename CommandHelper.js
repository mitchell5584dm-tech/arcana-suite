export function normalizeCommand(input) {
    const corrections = {
        "instal": "install",
        "instaall": "install",
        "subscrption": "subscription",
        "subscrip": "subscription",
        "updte": "update",
        "updat": "update",
        "confige": "config"
    };

    let output = input.toLowerCase();

    Object.keys(corrections).forEach(wrong => {
        if (output.includes(wrong)) {
            output = output.replace(wrong, corrections[wrong]);
        }
    });

    return output;
}

