class FaceDetector {
    constructor() {
        this.video = document.getElementById('video');
        this.canvas = document.getElementById('canvas');
        this.overlay = document.getElementById('overlay');
        this.ctx = this.canvas.getContext('2d');
        
        this.startTime = Date.now();
        this.detectionTime = null;
        this.scanningComplete = false;
        this.faceDetected = false;
        
        this.scanLinePos = 0;
        this.scanDirection = 1;
        
        this.targetUrl = "https://drive.google.com/file/d/1H5P4q7NQt3W7uYz62DTzYVx_Gx8XjxWy/view?usp=drivesdk";
    }
    
    async init() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
            this.video.srcObject = stream;
            await new Promise(resolve => {
                this.video.onloadedmetadata = resolve;
            });
            this.video.play();
            this.startDetection();
        } catch (error) {
            this.showOverlayText("CAMERA ACCESS DENIED", 30, 30);
            console.error("Error accessing camera:", error);
        }
    }
    
    startDetection() {
        const detect = async () => {
            const currentTime = Date.now();
            const elapsedTime = (currentTime - this.startTime) / 1000;
            
            if (!this.faceDetected && elapsedTime >= 20) {
                this.showOverlayText("TIMEOUT: NO FACE DETECTED", 30, 30);
                return;
            }
            
            this.ctx.drawImage(this.video, 0, 0, 640, 480);
            const frame = this.ctx.getImageData(0, 0, 640, 480);
            
            // Simple face detection using brightness and color variation
            const faces = this.detectFaces(frame);
            
            // Clear previous overlay
            this.overlay.innerHTML = '';
            
            // Draw tech border
            this.drawTechBorder();
            
            if (faces.length > 0) {
                if (!this.faceDetected) {
                    this.faceDetected = true;
                    this.detectionTime = currentTime;
                }
                
                // Draw face rectangles and targeting lines
                faces.forEach(face => {
                    this.drawTargetingEffects(face);
                });
                
                const timeSinceDetection = (currentTime - this.detectionTime) / 1000;
                if (timeSinceDetection <= 2.0) {
                    this.createSuccessAnimation(timeSinceDetection / 2.0);
                    this.showOverlayText("TARGET ACQUIRED!", 30, 30);
                    this.showOverlayText("GUEST VERIFICATION COMPLETE", 30, 60);
                } else {
                    window.open(this.targetUrl, '_blank');
                    return;
                }
            } else {
                // Scanning line effect
                this.drawScanningLine();
                
                this.showOverlayText("INITIALIZING FACE SCAN...", 30, 30);
                this.showOverlayText("AWAITING GUEST VERIFICATION", 30, 60);
                this.showOverlayText(`TIMEOUT IN: ${Math.max(0, 20 - elapsedTime).toFixed(1)}s`, 30, 90);
            }
            
            // Show timestamp
            const timestamp = new Date().toLocaleTimeString();
            this.showOverlayText(`TIME: ${timestamp}`, 30, this.canvas.height - 30);
            
            requestAnimationFrame(detect);
        };
        
        detect();
    }
    
    detectFaces(frame) {
        // Very basic face detection using brightness and color variation
        const width = frame.width;
        const height = frame.height;
        const data = frame.data;
        const faces = [];
        
        // Simple detection heuristic
        for (let y = 0; y < height; y += 20) {
            for (let x = 0; x < width; x += 20) {
                let brightPixels = 0;
                let colorVariation = 0;
                
                for (let dy = 0; dy < 20; dy++) {
                    for (let dx = 0; dx < 20; dx++) {
                        const idx = 4 * ((y + dy) * width + (x + dx));
                        const brightness = (data[idx] + data[idx+1] + data[idx+2]) / 3;
                        
                        if (brightness > 200) brightPixels++;
                        colorVariation += Math.abs(data[idx] - data[idx+1]) + 
                                          Math.abs(data[idx+1] - data[idx+2]) + 
                                          Math.abs(data[idx] - data[idx+2]);
                    }
                }
                
                if (brightPixels > 50 && colorVariation > 1000) {
                    faces.push({ x, y, width: 100, height: 100 });
                }
            }
        }
        
        return faces;
    }
    
    showOverlayText(text, x, y) {
        const textEl = document.createElement('div');
        textEl.textContent = text;
        textEl.className = 'overlay-text';
        textEl.style.left = `${x}px`;
        textEl.style.top = `${y}px`;
        this.overlay.appendChild(textEl);
    }
    
    drawTechBorder() {
        const ctx = this.ctx;
        const w = this.canvas.width;
        const h = this.canvas.height;
        const borderColor = 'rgba(0, 255, 255, 1)';
        const thickness = 2;
        const cornerLength = 30;
        const gap = 5;
        
        ctx.strokeStyle = borderColor;
        ctx.lineWidth = thickness;
        
        // Top-left
        ctx.beginPath();
        ctx.moveTo(gap, gap + cornerLength);
        ctx.lineTo(gap, gap);
        ctx.lineTo(gap + cornerLength, gap);
        ctx.stroke();
        
        // Top-right
        ctx.beginPath();
        ctx.moveTo(w - gap - cornerLength, gap);
        ctx.lineTo(w - gap, gap);
        ctx.lineTo(w - gap, gap + cornerLength);
        ctx.stroke();
        
        // Bottom-left
        ctx.beginPath();
        ctx.moveTo(gap, h - gap - cornerLength);
        ctx.lineTo(gap, h - gap);
        ctx.lineTo(gap + cornerLength, h - gap);
        ctx.stroke();
        
        // Bottom-right
        ctx.beginPath();
        ctx.moveTo(w - gap - cornerLength, h - gap);
        ctx.lineTo(w - gap, h - gap);
        ctx.lineTo(w - gap, h - gap - cornerLength);
        ctx.stroke();
    }
    
    drawTargetingEffects(face) {
        const ctx = this.ctx;
        const { x, y, width, height } = face;
        
        // Targeting box
        ctx.strokeStyle = 'rgba(0, 255, 255, 0.7)';
        ctx.lineWidth = 1;
        ctx.strokeRect(x - 2, y - 2, width + 4, height + 4);
        
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.5)';
        ctx.lineWidth = 1;
        ctx.strokeRect(x - 1, y - 1, width + 2, height + 2);
        
        // Targeting lines
        ctx.strokeStyle = 'rgba(0, 255, 255, 0.5)';
        ctx.beginPath();
        // Vertical line
        ctx.moveTo(x + width / 2, 0);
        ctx.lineTo(x + width / 2, y);
        ctx.moveTo(x + width / 2, y + height);
        ctx.lineTo(x + width / 2, this.canvas.height);
        
        // Horizontal line
        ctx.moveTo(0, y + height / 2);
        ctx.lineTo(x, y + height / 2);
        ctx.moveTo(x + width, y + height / 2);
        ctx.lineTo(this.canvas.width, y + height / 2);
        
        ctx.stroke();
    }
    
    drawScanningLine() {
        const ctx = this.ctx;
        
        ctx.strokeStyle = 'rgba(0, 255, 255, 0.7)';
        ctx.lineWidth = 1;
        
        ctx.beginPath();
        ctx.moveTo(0, this.scanLinePos);
        ctx.lineTo(this.canvas.width, this.scanLinePos);
        ctx.stroke();
        
        this.scanLinePos += 5 * this.scanDirection;
        
        if (this.scanLinePos >= this.canvas.height || this.scanLinePos <= 0) {
            this.scanDirection *= -1;
        }
    }
    
    createSuccessAnimation(progress) {
        const ctx = this.ctx;
        const centerX = this.canvas.width / 2;
        const centerY = this.canvas.height / 2;
        
        // Circular animation
        ctx.strokeStyle = 'rgba(0, 255, 255, 0.7)';
        ctx.lineWidth = 2;
        
        const radius = Math.min(this.canvas.width, this.canvas.height) * 0.8 * progress;
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
        ctx.stroke();
        
        // Checkmark animation
        if (progress > 0.5) {
            const lineProgress = (progress - 0.5) * 2;
            
            ctx.beginPath();
            ctx.moveTo(centerX - 40, centerY);
            
            const midX = centerX - 10;
            const midY = centerY + 30;
            const endX = centerX + 40;
            const endY = centerY - 20;
            
            const currentMidX = centerX - 40 + (midX - (centerX - 40)) * lineProgress;
            const currentMidY = centerY + (midY - centerY) * lineProgress;
            
            ctx.lineTo(currentMidX, currentMidY);
            
            if (progress > 0.75) {
                const currentEndX = currentMidX + (endX - currentMidX) * (lineProgress - 0.5) * 2;
                const currentEndY = currentMidY + (endY - currentMidY) * (lineProgress - 0.5) * 2;
                ctx.lineTo(currentEndX, currentEndY);
            }
            
            ctx.stroke();
        }
    }
}

// Initialize face detection on page load
document.addEventListener('DOMContentLoaded', () => {
    const detector = new FaceDetector();
    detector.init();
});
