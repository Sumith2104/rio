/**
 * =============================================================================
 * REVA SMART CAMPUS PLATFORM - SMTP NODEMAILER NOTIFICATION DISPATCHER
 * Author: Sumith U (SRN: R24EA807), 7th Sem B.Tech CSE (AI & ML), REVA University
 * =============================================================================
 * Dispatches automated institutional student notifications using:
 *   1. Faculty Document / Lecture Notes Uploads (ChromaDB vectorization alerts)
 *   2. Course Assignments & Problem Distributions (Due date, rubrics, max marks)
 *   3. Attendance Updates & Low Attendance Early Warnings (Mandatory 75% threshold)
 * =============================================================================
 */

const path = require('path');
require('dotenv').config({ path: path.join(__dirname, '.env') });
const nodemailer = require('nodemailer');

function parseArgs() {
    const args = process.argv.slice(2);
    const parsed = {
        type: 'doc_upload', // 'doc_upload', 'assignment', 'attendance', 'otp'
        to: '',
        name: 'Sumith U',
        entityId: 'R24EA807',
        title: '',
        unit: 'Unit 3: Deep Neural Networks',
        uploadedBy: 'Dr. Ramesh Kumar',
        dueDate: '2026-11-10',
        marks: '10 Marks',
        att: '68.0%',
        threshold: '75.0%',
        course: 'AIML-401 Deep Learning',
        otp: ''
    };

    for (let i = 0; i < args.length; i++) {
        if (args[i] === '--type' && args[i + 1]) parsed.type = args[++i];
        else if (args[i] === '--to' && args[i + 1]) parsed.to = args[++i];
        else if (args[i] === '--name' && args[i + 1]) parsed.name = args[++i];
        else if (args[i] === '--entityId' && args[i + 1]) parsed.entityId = args[++i];
        else if (args[i] === '--title' && args[i + 1]) parsed.title = args[++i];
        else if (args[i] === '--unit' && args[i + 1]) parsed.unit = args[++i];
        else if (args[i] === '--uploadedBy' && args[i + 1]) parsed.uploadedBy = args[++i];
        else if (args[i] === '--dueDate' && args[i + 1]) parsed.dueDate = args[++i];
        else if (args[i] === '--marks' && args[i + 1]) parsed.marks = args[++i];
        else if (args[i] === '--att' && args[i + 1]) parsed.att = args[++i];
        else if (args[i] === '--threshold' && args[i + 1]) parsed.threshold = args[++i];
        else if (args[i] === '--course' && args[i + 1]) parsed.course = args[++i];
        else if (args[i] === '--otp' && args[i + 1]) parsed.otp = args[++i];
    }
    return parsed;
}

function buildHtmlTemplate(params) {
    const { type, to, name, entityId, title, unit, uploadedBy, dueDate, marks, att, threshold, course, otp } = params;

    let badgeText = "CAMPUS NOTIFICATION";
    let badgeColor = "#2563eb";
    let subjectHeader = "Academic Notification";
    let bodyContent = "";

    if (type === 'doc_upload') {
        badgeText = "NEW COURSE MATERIAL";
        badgeColor = "#0284c7";
        subjectHeader = "New Faculty Learning Material Uploaded";
        bodyContent = `
          <p style="font-size: 14px; line-height: 1.6; color: #334155;">
            Faculty member <strong>${uploadedBy}</strong> has uploaded new curriculum study material for <strong>${course}</strong>.
            This document has been indexed into the ChromaDB vector database and is available for your autonomous AI tutor.
          </p>
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-left: 4px solid #0284c7; padding: 16px; border-radius: 8px; margin: 20px 0;">
            <div style="font-size: 11px; text-transform: uppercase; color: #64748b; font-weight: 700;">Document Title</div>
            <div style="font-size: 16px; font-weight: 700; color: #0f172a; margin: 4px 0;">${title || 'Lecture Notes & Blueprint'}</div>
            <div style="font-size: 13px; color: #475569;">Curriculum Module: <strong>${unit}</strong></div>
            <div style="font-size: 12px; color: #16a34a; font-weight: 600; margin-top: 6px;">&check; Ready in Student Portal &bull; RAG Vector Store Active</div>
          </div>
          <p style="font-size: 13px; color: #64748b;">
            You can query your AI Copilot in the Student Portal for detailed explanations, formulas, and topic-wise derivations from this document.
          </p>
        `;
    } else if (type === 'assignment') {
        badgeText = "NEW ASSIGNMENT";
        badgeColor = "#7c3aed";
        subjectHeader = "Course Assignment Distributed";
        bodyContent = `
          <p style="font-size: 14px; line-height: 1.6; color: #334155;">
            A new homework assignment has been distributed for <strong>${course}</strong>.
            Please submit your handwritten solution scan or typed formulation before the deadline.
          </p>
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-left: 4px solid #7c3aed; padding: 16px; border-radius: 8px; margin: 20px 0;">
            <div style="font-size: 11px; text-transform: uppercase; color: #64748b; font-weight: 700;">Task Overview</div>
            <div style="font-size: 16px; font-weight: 700; color: #0f172a; margin: 4px 0;">${title || 'Unit Assignment'}</div>
            <table style="width: 100%; font-size: 13px; margin-top: 8px;">
              <tr><td style="color: #64748b; padding: 3px 0;">Due Date:</td><td style="font-weight: 600; color: #b91c1c;">${dueDate}</td></tr>
              <tr><td style="color: #64748b; padding: 3px 0;">Max Marks:</td><td style="font-weight: 600; color: #0f172a;">${marks}</td></tr>
              <tr><td style="color: #64748b; padding: 3px 0;">Evaluation:</td><td style="font-weight: 600; color: #0f172a;">AI Vision OCR &amp; Grounded Rubric Scoring</td></tr>
            </table>
          </div>
        `;
    } else if (type === 'attendance') {
        const isCritical = parseFloat(att) < 75.0;
        badgeText = isCritical ? "CRITICAL ATTENDANCE ALERT" : "ATTENDANCE UPDATE";
        badgeColor = isCritical ? "#dc2626" : "#eab308";
        subjectHeader = isCritical ? "Mandatory Attendance Threshold Warning (< 75%)" : "Academic Attendance Update";
        bodyContent = `
          <p style="font-size: 14px; line-height: 1.6; color: #334155;">
            Your academic attendance record in <strong>${course}</strong> has been updated.
            ${isCritical ? 'Your cumulative attendance has fallen below the mandatory University threshold of 75.0%.' : 'Your attendance is currently within satisfactory academic standing.'}
          </p>
          <div style="background: #fef2f2; border: 1px solid #fecaca; border-left: 4px solid #dc2626; padding: 18px; border-radius: 8px; margin: 20px 0;">
            <div style="font-size: 11px; text-transform: uppercase; color: #991b1b; font-weight: 700;">Current Record</div>
            <div style="font-size: 32px; font-weight: 800; color: ${isCritical ? '#b91c1c' : '#15803d'}; margin: 4px 0;">${att}</div>
            <div style="font-size: 13px; color: #7f1d1d;">Mandatory REVA Threshold: <strong>${threshold}</strong></div>
            ${isCritical ? `
              <div style="font-size: 12px; color: #991b1b; margin-top: 10px; padding-top: 8px; border-top: 1px dashed #fca5a5;">
                <strong>Action Required:</strong> You must attend the next <strong>6 consecutive lectures</strong> without absence to recover your eligibility for the end-semester examinations.
              </div>
            ` : ''}
          </div>
        `;
    } else {
        // Fallback OTP
        badgeText = "AUTHENTICATION";
        badgeColor = "#0f172a";
        subjectHeader = "One-Time Verification Passcode";
        bodyContent = `
          <div style="text-align: center; background: #f1f5f9; padding: 18px; border-radius: 10px; margin: 20px 0;">
            <div style="font-size: 36px; font-weight: 800; letter-spacing: 8px; font-family: monospace;">${otp}</div>
            <div style="font-size: 12px; color: #e11d48; margin-top: 6px; font-weight: 600;">Valid for 10 minutes</div>
          </div>
        `;
    }

    return `
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>${subjectHeader}</title>
      <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f8fafc; margin: 0; padding: 24px; color: #1e293b; }
        .card { max-width: 560px; margin: 0 auto; background: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 4px 16px rgba(0,0,0,0.06); overflow: hidden; }
        .header { background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); padding: 26px 24px; color: #ffffff; text-align: center; }
        .header h1 { margin: 0; font-size: 20px; font-weight: 700; letter-spacing: -0.5px; }
        .header p { margin: 6px 0 0; font-size: 13px; color: #94a3b8; }
        .badge { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 700; text-transform: uppercase; background: ${badgeColor}; color: #ffffff; margin-top: 10px; }
        .body { padding: 32px 24px; }
        .greeting { font-size: 15px; margin-bottom: 12px; }
        .info-table { width: 100%; border-collapse: collapse; margin-top: 20px; font-size: 12.5px; border-top: 1px solid #f1f5f9; }
        .info-table td { padding: 6px 0; color: #64748b; }
        .info-table td.val { color: #0f172a; font-weight: 600; text-align: right; }
        .btn-action { display: inline-block; background: #0f172a; color: #ffffff !important; padding: 10px 20px; border-radius: 7px; text-decoration: none; font-size: 13px; font-weight: 600; margin-top: 14px; }
        .footer { background: #f8fafc; border-top: 1px solid #f1f5f9; padding: 18px 24px; text-align: center; font-size: 12px; color: #64748b; }
      </style>
    </head>
    <body>
      <div class="card">
        <div class="header">
          <h1>REVA Smart Campus Intelligence</h1>
          <p>School of Computing &amp; IT &bull; PACD-RAG Platform</p>
          <span class="badge">${badgeText}</span>
        </div>
        <div class="body">
          <p class="greeting">Dear <strong>${name}</strong> (${entityId}),</p>
          ${bodyContent}
          <div style="text-align: center; margin: 24px 0 16px;">
            <a href="http://localhost:8002/#student" class="btn-action">Open Student Portal &rarr;</a>
          </div>
          <table class="info-table">
            <tr><td>Recipient Student:</td><td class="val">${name} (${entityId})</td></tr>
            <tr><td>Verified Email:</td><td class="val">${to}</td></tr>
            <tr><td>Notification Type:</td><td class="val">${badgeText}</td></tr>
            <tr><td>Timestamp (IST):</td><td class="val">${new Date().toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' })}</td></tr>
          </table>
        </div>
        <div class="footer">
          School of Computing & IT &bull; REVA University, Bengaluru, India<br>
          Autonomous Student Academic Intelligence &amp; Copilot
        </div>
      </div>
    </body>
    </html>
    `;
}

async function createSmtpTransporter() {
    const smtpHost = process.env.SMTP_HOST;
    const smtpPort = parseInt(process.env.SMTP_PORT || '587', 10);
    const smtpUser = process.env.SMTP_USER;
    const smtpPass = process.env.SMTP_PASS;

    if (smtpHost && smtpUser && smtpPass) {
        return {
            transporter: nodemailer.createTransport({
                host: smtpHost,
                port: smtpPort,
                secure: smtpPort === 465,
                auth: { user: smtpUser, pass: smtpPass },
                connectionTimeout: 5000,
                greetingTimeout: 5000,
                socketTimeout: 5000
            }),
            type: 'live-smtp',
            from: process.env.SMTP_FROM || `"REVA Smart Campus" <${smtpUser}>`
        };
    }

    try {
        const testAccount = await nodemailer.createTestAccount();
        const etherealTransporter = nodemailer.createTransport({
            host: testAccount.smtp.host,
            port: testAccount.smtp.port,
            secure: testAccount.smtp.secure,
            auth: {
                user: testAccount.user,
                pass: testAccount.pass
            },
            connectionTimeout: 5000,
            greetingTimeout: 5000,
            socketTimeout: 5000
        });
        return {
            transporter: etherealTransporter,
            type: 'ethereal-smtp',
            from: '"REVA Smart Campus Alerts" <alerts@reva.edu.in>'
        };
    } catch (err) {
        const jsonTransporter = nodemailer.createTransport({
            jsonTransport: true
        });
        return {
            transporter: jsonTransporter,
            type: 'json-fallback',
            from: '"REVA Smart Campus Alerts" <alerts@reva.edu.in>'
        };
    }
}

async function main() {
    const params = parseArgs();
    if (!params.to) {
        console.error(JSON.stringify({
            success: false,
            error: 'Missing required argument: --to is required.'
        }));
        process.exit(1);
    }

    try {
        const { transporter, type, from } = await createSmtpTransporter();
        const recipient = process.env.SMTP_FORWARD_TO || params.to;

        let subject = `[REVA Campus] Academic Notification for ${params.name}`;
        if (params.type === 'doc_upload') {
            subject = `📚 [REVA Campus] New Notes Uploaded: ${params.title || 'Course Lecture Notes'}`;
        } else if (params.type === 'assignment') {
            subject = `📝 [REVA Campus] New Assignment: ${params.title || 'Homework Assignment'}`;
        } else if (params.type === 'attendance') {
            subject = `⚠️ [REVA Campus] Attendance Notice: ${params.att} (Threshold: 75.0%)`;
        } else if (params.type === 'otp') {
            subject = `🔐 [REVA Campus] Security Code: ${params.otp}`;
        }

        const mailOptions = {
            from: from,
            to: recipient,
            subject: subject,
            text: `REVA SMART CAMPUS NOTIFICATION\n\nHello ${params.name} (${params.entityId}),\n\n${subject}\n\nLog in to your Student Portal to view: http://localhost:8002/#student`,
            html: buildHtmlTemplate(params)
        };

        const info = await transporter.sendMail(mailOptions);
        const previewUrl = nodemailer.getTestMessageUrl(info) || null;

        console.log(JSON.stringify({
            success: true,
            transport: type,
            messageId: info.messageId,
            previewUrl: previewUrl,
            to: recipient,
            type: params.type,
            title: params.title,
            studentName: params.name,
            entityId: params.entityId,
            dispatchedAt: new Date().toISOString()
        }));
    } catch (error) {
        console.error(JSON.stringify({
            success: false,
            error: error.message
        }));
        process.exit(1);
    }
}

main();
