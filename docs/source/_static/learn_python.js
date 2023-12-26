$(document).ready(function () {
    $('a.external').attr('target', '_blank');

    document.querySelectorAll(".use-termynal").forEach(node => {
        node.style.display = "block";
        new Termynal(node, {
            lineDelay: 500
        });
    });
    createTermynals();
    loadVisibleTermynals();
});


const progressLiteralStart = "---> 100%";
const promptLiteralStart = "?> ";
const customPromptLiteralStart = "# ";
const termynalActivateClass = "highlight-console";
let termynals = [];


function parseConsoleLine(str) {
    const parenthesesRegex = /(?:\(([^)]+)\))?\?>(.*)/;
    const match = parenthesesRegex.exec(str);

    if (!match) return null;

    const line = match[2];
    const variables = match[1] || '';

    // Regular expression to match 'variable_name=value'
    const pairRegex = /(\w+)=(\w+)/g;
    
    const result = {
        type: 'input',
        value: line,
    };
    let pairMatch;

    // Iterate over each 'variable_name=value' pair
    while ((pairMatch = pairRegex.exec(variables)) !== null) {
        // Extract variable name and value
        const [_, key, value] = pairMatch;
        // Add to the result object
        result[key] = value;
    }

    return result;
}

function createTermynals() {
    document
        .querySelectorAll(`.${termynalActivateClass} .highlight`)
        .forEach(node => {
            const text = node.textContent;
            const lines = text.split("\n");
            if (lines[lines.length - 1] === "") {
                lines.pop();
            }
            const useLines = [];
            let buffer = [];
            let lineData = {};
            function saveBuffer() {
                if (buffer.length) {
                    let isBlankSpace = true;
                    buffer.forEach(line => {
                        if (line) {
                            isBlankSpace = false;
                        }
                    });
                    dataValue = {};
                    if (isBlankSpace) {
                        dataValue["delay"] = 0;
                    }
                    if (buffer[buffer.length - 1] === "") {
                        // A last single <br> won't have effect
                        // so put an additional one
                        buffer.push("");
                    }
                    const bufferValue = buffer.join("<br>");
                    dataValue["value"] = bufferValue;
                    useLines.push(dataValue);
                    buffer = [];
                }
            }
            for (let line of lines) {
                lineData = parseConsoleLine(line);
                if (lineData) {
                    saveBuffer();
                    useLines.push(lineData);
                }
                else if (line === progressLiteralStart) {
                    saveBuffer();
                    useLines.push({
                        type: "progress"
                    });
                } else if (line.startsWith("// ")) {
                    saveBuffer();
                    const value = "💬 " + line.replace("// ", "").trimEnd();
                    useLines.push({
                        value: value,
                        class: "termynal-comment",
                        delay: 0
                    });
                } else if (line.startsWith(customPromptLiteralStart)) {
                    saveBuffer();
                    const promptStart = line.indexOf(promptLiteralStart);
                    if (promptStart === -1) {
                        console.error("Custom prompt found but no end delimiter", line)
                    }
                    const prompt = line.slice(0, promptStart).replace(customPromptLiteralStart, "")
                    let value = line.slice(promptStart + promptLiteralStart.length);
                    useLines.push({
                        type: "input",
                        value: value,
                        prompt: prompt
                    });
                } else {
                    buffer.push(line);
                }
            }
            saveBuffer();
            const div = document.createElement("div");
            node.replaceWith(div);
            const termynal = new Termynal(div, {
                lineData: useLines,
                noInit: true,
                startDelay: 650,
                typeDelay: 50,
                lineDelay: 0
            });
            termynals.push(termynal);
        });
}

function loadVisibleTermynals() {
    termynals = termynals.filter(termynal => {
        if (termynal.container.getBoundingClientRect().top - innerHeight <= 0) {
            termynal.init();
            return false;
        }
        return true;
    });
}
window.addEventListener("scroll", loadVisibleTermynals);
