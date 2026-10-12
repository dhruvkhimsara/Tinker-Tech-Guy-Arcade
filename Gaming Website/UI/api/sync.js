export default async function handler(req, res) {
    // Allow requests from your frontend
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    const GIST_ID = process.env.GIST_ID;
    const GIST_TOKEN = process.env.GIST_TOKEN;

    if (!GIST_ID || !GIST_TOKEN) {
        return res.status(500).json({ error: 'Server configuration error: Missing Gist credentials.' });
    }

    try {
        if (req.method === 'GET') {
            // Fetch database from GitHub Gist
            const response = await fetch(`https://api.github.com/gists/${GIST_ID}`, {
                headers: { 'Authorization': `token ${GIST_TOKEN}` }
            });
            const data = await response.json();
            const fileContent = data.files['arcade_db.json'].content;
            return res.status(200).json(JSON.parse(fileContent));
        }

        if (req.method === 'POST') {
            // Update database on GitHub Gist
            const updatedData = req.body;

            const response = await fetch(`https://api.github.com/gists/${GIST_ID}`, {
                method: 'PATCH',
                headers: {
                    'Authorization': `token ${GIST_TOKEN}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    files: {
                        'arcade_db.json': {
                            content: JSON.stringify(updatedData, null, 2)
                        }
                    }
                })
            });

            if (!response.ok) {
                throw new Error('Failed to update Gist on GitHub');
            }

            return res.status(200).json({ success: true });
        }

        return res.status(405).json({ error: 'Method not allowed' });
    } catch (err) {
        console.error(err);
        return res.status(500).json({ error: 'Internal server error' });
    }
}