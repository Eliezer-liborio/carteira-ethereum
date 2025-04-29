// static/index.js
let web3;

async function connectWallet() {
    if (typeof window.ethereum !== 'undefined') {
        web3 = new Web3(window.ethereum);
        await window.ethereum.request({ method: 'eth_requestAccounts' });

        const accounts = await web3.eth.getAccounts();
        const address = accounts[0];

        const nonceResp = await fetch("/get_nonce", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ address })
        });

        const { nonce } = await nonceResp.json();
        const message = `Login HakaiChain - Nonce: ${nonce}`;

        const signature = await web3.eth.personal.sign(message, address);

        const verifyResp = await fetch("/verify", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ address, signature, message })
        });

        const result = await verifyResp.json();
        alert(result.status === "success" ? `Token: ${result.token}` : "Falha na autenticação");
    } else {
        alert("Instale a MetaMask!");
    }
}
