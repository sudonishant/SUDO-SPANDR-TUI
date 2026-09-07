"""Chapter 5: Mathematical & Algorithmic Foundations"""

def get_chapter_5_html() -> str:
    return r"""
<h1>5. Mathematical & Algorithmic Foundations</h1>

<h2>5.1 Shannon Information Entropy Theory in Payload Forensics</h2>
<p>
A cornerstone of modern binary reverse engineering and malware pathology is the mathematical measurement of information density. In 1948, Claude Shannon published his seminal work, <em>"A Mathematical Theory of Communication,"</em> defining information entropy as a measure of the uncertainty or randomness inherent in a variable or stream of discrete data. In <strong>SUDO SPANDR</strong>, this mathematical foundation is adapted directly to the byte-level inspection of email attachments and body bitstreams.
</p>

<h3>5.1.1 Formal Mathematical Definition</h3>
<p>
Let an extracted binary bitstream or carved payload be represented as a discrete random variable $X$, consisting of $N$ total bytes drawn from an alphabet $\mathcal{A}$ of possible byte values ranging from <code>0x00</code> to <code>0xFF</code> ($|\mathcal{A}| = 256$). The probability $P(x_i)$ of occurrence for any specific byte value $x_i \in \mathcal{A}$ is defined as:
</p>

<div class="math-equation">
    P(x_i) = \frac{f(x_i)}{N} = \frac{\sum_{k=1}^{N} \mathbb{I}(b_k = x_i)}{N}
</div>

<p>
where $f(x_i)$ is the observed frequency of byte $x_i$ within the buffer, and $\mathbb{I}$ is the indicator function. The Shannon entropy $H(X)$, expressed in bits per byte, is rigorously computed as:
</p>

<div class="math-equation">
    H(X) = -\sum_{i=0}^{255} P(x_i) \log_2 P(x_i)
</div>

<p>
with the mathematical convention that if $P(x_i) = 0$, then $0 \log_2(0) = 0$. Since the alphabet size is 256 ($2^8$), the theoretical maximum entropy for any byte distribution is:
</p>

<div class="math-equation">
    H_{\max} = \log_2(256) = 8.0000 \text{ bits per byte}
</div>

<h3>5.1.2 Forensic Interpretation & Classification Thresholds</h3>
<p>
The calculated Shannon entropy value directly indicates the underlying physical structure of the carved payload:
</p>

<table>
    <thead>
        <tr>
            <th>Entropy Score Range ($H$)</th>
            <th>Physical Structural Characteristics</th>
            <th>Typical File & Payload Typology</th>
            <th>Forensic Threat Status</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>$0.00 \le H < 3.50$</strong></td>
            <td>Extreme uniformity, massive repetition of zero bytes or whitespace.</td>
            <td>Sparse binary arrays, unformatted ASCII logs, raw memory dumps.</td>
            <td>BENIGN / LOW RISK</td>
        </tr>
        <tr>
            <td><strong>$3.50 \le H < 5.20$</strong></td>
            <td>Structured natural language text with typical character frequency distributions.</td>
            <td>Plaintext English emails, standard HTML/CSS code, basic source scripts.</td>
            <td>BENIGN / LOW RISK</td>
        </tr>
        <tr>
            <td><strong>$5.20 \le H < 6.80$</strong></td>
            <td>Compiled machine instructions with varying opcodes, ASCII strings, and import tables.</td>
            <td>Standard uncompressed PE32/ELF executables, uncompressed PDF structures.</td>
            <td>NORMAL EXECUTABLE</td>
        </tr>
        <tr>
            <td><strong>$6.80 \le H < 7.20$</strong></td>
            <td>Moderate compression or algorithmic encoding.</td>
            <td>JPEG/PNG imagery, gzip compressed streams, standard ZIP archives.</td>
            <td>ELEVATED / INSPECT</td>
        </tr>
        <tr>
            <td><strong>$7.20 \le H \le 8.00$</strong></td>
            <td>Near-perfect pseudorandom distribution, minimal repeating patterns.</td>
            <td>UPX/Themida packed binaries, encrypted ransomware droppers, polymorphic shellcode.</td>
            <td>CRITICAL MALWARE ALERT</td>
        </tr>
    </tbody>
</table>

<div class="callout danger">
    <div class="callout-title">🚨 The Cryptographic Packing Paradox</div>
    <p>
    Malware authors utilize runtime packers (such as UPX, VMProtect, or custom XOR/AES crypters) to conceal malicious strings and API import tables from static signature engines. However, this encryption process inadvertently increases the byte entropy to near theoretical maximums ($H > 7.6$). SUDO SPANDR leverages this physical property: whenever an attachment claiming to be a document (e.g., <code>.pdf</code> or <code>.docx</code>) exhibits an entropy score exceeding $7.2$, the system flags it as a <strong>Packed Weaponized Dropper</strong>.
    </p>
</div>

<h2>5.2 String Distance Metrics & Homoglyph Collision Mathematics</h2>
<p>
A primary attack vector in spear-phishing and Business Email Compromise is the registration of visually deceptive domains. Threat actors register lookalike domains targeting high-value corporate, government, or banking institutions (e.g., registering <code>micros0ft.com</code> instead of <code>microsoft.com</code>, or substituting Latin letters with Cyrillic glyphs). SUDO SPANDR applies rigorous string metric mathematics to quantify this divergence.
</p>

<h3>5.2.1 Levenshtein & Damerau-Levenshtein Edit Distance</h3>
<p>
The Levenshtein distance between two strings $s_1$ and $s_2$ represents the minimum number of single-character edit operations (insertions, deletions, or substitutions) required to transform $s_1$ into $s_2$. Mathematically, for strings of length $|s_1|$ and $|s_2|$, the distance matrix $D(i, j)$ is computed via dynamic programming:
</p>

<div class="math-equation">
    D(i, j) = \begin{cases} 
    \max(i, j) & \text{if } \min(i, j) = 0, \\
    \min \begin{cases} 
        D(i-1, j) + 1 \\ 
        D(i, j-1) + 1 \\ 
        D(i-1, j-1) + \mathbb{I}(s_1[i] \neq s_2[j]) 
    \end{cases} & \text{otherwise.}
    \end{cases}
</div>

<p>
SUDO SPANDR extends this using the <strong>Damerau-Levenshtein distance</strong>, which accounts for character transpositions ($s_1[i] = s_2[j-1]$ and $s_1[i-1] = s_2[j]$), a common typo-squatting tactic (e.g., <code>amzon.com</code> vs <code>amazon.com</code>).
</p>

<h3>5.2.2 Normalized Similarity Ratio</h3>
<p>
To compare strings of differing lengths objectively, the engine computes a normalized similarity coefficient $S(s_1, s_2) \in [0, 1]$:
</p>

<div class="math-equation">
    S(s_1, s_2) = 1.0 - \frac{D(s_1, s_2)}{\max(|s_1|, |s_2|)}
</div>

<p>
If $S(s_1, s_2) \ge 0.80$ against any domain in the protected institutional whitelist (e.g., major Indian banks, government portals like <code>gov.in</code>, <code>nic.in</code>, or global technology providers), but $s_1 \neq s_2$, the domain is mathematically flagged as an active <strong>Typo-Squatting / Phishing Impersonation Attack</strong>.
</p>

<h3>5.2.3 Unicode Homoglyph Collision Matrix</h3>
<p>
The Unicode Standard contains thousands of distinct glyphs across multiple scripts that render identically or near-identically on modern displays. For example:
</p>
<ul>
    <li>Latin Small Letter <code>'a'</code> (<code>U+0061</code>) vs. Cyrillic Small Letter <code>'а'</code> (<code>U+0430</code>)</li>
    <li>Latin Small Letter <code>'o'</code> (<code>U+006F</code>) vs. Cyrillic Small Letter <code>'о'</code> (<code>U+043E</code>)</li>
    <li>Latin Small Letter <code>'e'</code> (<code>U+0065</code>) vs. Cyrillic Small Letter <code>'е'</code> (<code>U+0435</code>)</li>
    <li>Latin Small Letter <code>'p'</code> (<code>U+0070</code>) vs. Cyrillic Small Letter <code>'р'</code> (<code>U+0440</code>)</li>
</ul>
<p>
When an adversary registers a domain using Cyrillic <code>'а'</code> (e.g., <code>pаypal.com</code>), the DNS system encodes it using <strong>Punycode (RFC 3492)</strong> as <code>xn--pypal-4ve.com</code>. SUDO SPANDR implements a bidirectional homoglyph mapping table. When a domain is parsed:
</p>
<ol>
    <li>It checks if the domain begins with <code>xn--</code>; if true, it decodes the Punycode into its full Unicode representation.</li>
    <li>It inspects every character for <strong>mixed-script anomalies</strong> (combining Latin and Cyrillic/Greek scripts within a single label).</li>
    <li>It maps all confusable Unicode characters back to their ASCII canonical equivalents and compares the normalized string against target enterprise domains. If a collision occurs, a <strong>Critical IDN Homograph Spoof</strong> is confirmed.</li>
</ol>

<h2>5.3 Graph-Theoretic Reconstruction of Mail Relay Transit Topology</h2>
<p>
The transmission of an electronic mail across the global internet can be formally modeled as traversal through a <strong>Directed Acyclic Graph (DAG)</strong>:
</p>

<div class="math-equation">
    G = (V, E)
</div>

<p>
where each vertex $v \in V$ represents a Mail Transfer Agent (MTA), characterized by an IP address $IP(v)$, a resolved hostname $H(v)$, and an internal clock $T(v)$. Each directed edge $(v_i, v_{i+1}) \in E$ represents an SMTP transmission relay from MTA $v_i$ to MTA $v_{i+1}$.
</p>

<h3>5.3.1 Topological Ordering & Latency Calculations</h3>
<p>
Because intermediate MTAs prepend <code>Received:</code> headers to the top of the header stack, the physical header order in an <code>.eml</code> file is reverse-chronological. SUDO SPANDR executes a bottom-up topological sorting algorithm:
</p>
<ol>
    <li>The lowest <code>Received:</code> header is designated as the origin hop $v_0$ (the originating submission client or first boundary MTA).</li>
    <li>Subsequent headers are indexed sequentially $v_1, v_2, \dots, v_n$, where $v_n$ represents the final recipient's MX gateway.</li>
    <li>For each adjacent pair of hops $(v_i, v_{i+1})$, the transit latency delta $\Delta t_i$ is computed:
        <div class="math-equation">
            \Delta t_i = T(v_{i+1}) - T(v_i)
        </div>
    </li>
</ol>

<h3>5.3.2 Anomaly Detection via Graph Constraints</h3>
<p>
In an authentic, unmanipulated transmission path, the following graph-theoretic invariants must hold:
</p>
<ul>
    <li><strong>Temporal Monotonicity:</strong> $\forall i \in [0, n-1], \Delta t_i \ge 0$. A negative delta ($\Delta t_i < 0$) indicates either an uncalibrated NTP daemon or forged headers injected by an adversary to conceal the originating IP address.</li>
    <li><strong>Routability Transitions:</strong> The origin hop $v_0$ may possess an RFC 1918 private IP address (e.g., <code>10.0.0.0/8</code>, <code>192.168.0.0/16</code>), representing an internal corporate workstation. However, once the email transitions to a public IP at $v_1$, no subsequent hop $v_k$ ($k > 1$) may revert to a private RFC 1918 address until the final destination corporate gateway is reached. An intermediate private hop indicates an internal relay loop or forged transit headers.</li>
</ul>
"""
