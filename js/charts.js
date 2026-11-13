/**
 * AI-Powered Smart Campus Intelligence & Student Success Platform
 * Chart Manager (Chart.js Integration)
 * Author: Sumith U (SRN: R24EA807) - REVA University
 * Design: Minimalist Monochrome (White, Black, and Grey only)
 */

let charts = {};

// Monochromatic Theme Options for Chart.js
const chartTheme = {
  color: '#374151',
  borderColor: 'rgba(0, 0, 0, 0.08)',
  font: {
    family: "'Inter', sans-serif",
    size: 11,
    weight: '500'
  }
};

function initAllCharts() {
  initTrajectoryChart();
  initSalEcChart();
  initDeptRiskChart();
  initSrlHabitChart();
}

/**
 * 1. Conv-LSTM Week-Wise Early Prediction Trajectory (Chen et al. 2022)
 * Demonstrates early detection capability starting from Week 4-6
 */
function initTrajectoryChart() {
  const ctx = document.getElementById('trajectoryChart');
  if (!ctx) return;

  if (charts.trajectory) charts.trajectory.destroy();

  charts.trajectory = new Chart(ctx, {
    type: 'line',
    data: {
      labels: CAMPUS_ANALYTICS.weeklyTemporalTrend.weeks,
      datasets: [
        {
          label: 'Conv-LSTM Accuracy (%)',
          data: CAMPUS_ANALYTICS.weeklyTemporalTrend.convLstmAccuracy,
          borderColor: '#000000',
          backgroundColor: 'rgba(0, 0, 0, 0.05)',
          borderWidth: 2.5,
          tension: 0.35,
          fill: true,
          pointBackgroundColor: '#000000',
          pointHoverRadius: 6
        },
        {
          label: 'Conv-LSTM Recall (%)',
          data: CAMPUS_ANALYTICS.weeklyTemporalTrend.convLstmRecall,
          borderColor: '#4B5563',
          backgroundColor: 'transparent',
          borderWidth: 2,
          borderDash: [5, 4],
          tension: 0.35,
          pointBackgroundColor: '#4B5563',
          pointHoverRadius: 6
        },
        {
          label: 'Identified At-Risk Students',
          data: CAMPUS_ANALYTICS.weeklyTemporalTrend.atRiskPopulationIdentified,
          borderColor: '#9CA3AF',
          backgroundColor: 'rgba(0, 0, 0, 0.02)',
          borderWidth: 2,
          yAxisID: 'yCount',
          tension: 0.3,
          pointBackgroundColor: '#9CA3AF'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top',
          labels: { color: chartTheme.color, font: chartTheme.font, usePointStyle: true, boxWidth: 8 }
        },
        tooltip: {
          backgroundColor: '#111827',
          titleColor: '#FFFFFF',
          bodyColor: '#D1D5DB',
          borderColor: '#374151',
          borderWidth: 1,
          padding: 10,
          callbacks: {
            footer: (items) => {
              if (items[0].label === 'W6') return 'Key Early-Warning Benchmark (Chen et al.: Recall 0.91)';
              return '';
            }
          }
        }
      },
      scales: {
        x: {
          grid: { color: 'rgba(0, 0, 0, 0.05)' },
          ticks: { color: chartTheme.color, font: chartTheme.font }
        },
        y: {
          min: 50,
          max: 100,
          grid: { color: 'rgba(0, 0, 0, 0.06)' },
          ticks: {
            color: chartTheme.color,
            font: chartTheme.font,
            callback: (v) => v + '%'
          },
          title: { display: true, text: 'Model Accuracy / Recall', color: chartTheme.color, font: { size: 10 } }
        },
        yCount: {
          position: 'right',
          min: 0,
          max: 100,
          grid: { display: false },
          ticks: { color: '#4B5563', font: chartTheme.font },
          title: { display: true, text: 'At-Risk Count', color: '#4B5563', font: { size: 10 } }
        }
      }
    }
  });
}

/**
 * 2. SAL & EC Dual-Factor Matrix (Qin et al. 2023)
 * Maps Student Academic Level (SAL) vs External Characteristics (EC)
 */
function initSalEcChart() {
  const ctx = document.getElementById('salEcChart');
  if (!ctx) return;

  if (charts.salEc) charts.salEc.destroy();

  const dataPoints = STUDENTS_DATABASE.map(s => ({
    x: s.salScore,
    y: s.ecScore,
    student: s,
    r: s.riskCategory === 'High' ? 9 : s.riskCategory === 'Medium' ? 7 : 5
  }));

  charts.salEc = new Chart(ctx, {
    type: 'bubble',
    data: {
      datasets: [{
        label: 'Monitored Students',
        data: dataPoints,
        backgroundColor: (context) => {
          const item = context.raw?.student;
          if (!item) return '#9CA3AF';
          if (item.riskCategory === 'High') return 'rgba(0, 0, 0, 0.85)';
          if (item.riskCategory === 'Medium') return 'rgba(75, 85, 99, 0.75)';
          return 'rgba(209, 213, 219, 0.8)';
        },
        borderColor: '#111827',
        borderWidth: 1.5,
        hoverRadius: 10
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#111827',
          titleColor: '#FFFFFF',
          bodyColor: '#D1D5DB',
          callbacks: {
            title: (items) => {
              const item = items[0].raw?.student;
              return item ? `${item.name} (${item.srn})` : '';
            },
            label: (item) => {
              const s = item.raw?.student;
              if (!s) return '';
              return [
                `Risk Tier: ${s.riskCategory} (${s.riskScore}%)`,
                `SAL (Academic Level): ${s.salScore}/100`,
                `EC (Context Score): ${s.ecScore}/100`,
                `CGPA: ${s.cgpa} | VLE Hours: ${s.vleStudyHoursWeekly}h/wk`
              ];
            }
          }
        }
      },
      scales: {
        x: {
          min: 20,
          max: 100,
          grid: { color: 'rgba(0, 0, 0, 0.05)' },
          ticks: { color: chartTheme.color, font: chartTheme.font },
          title: { display: true, text: 'Student Academic Level (SAL) Score', color: chartTheme.color, font: { size: 10 } }
        },
        y: {
          min: 20,
          max: 100,
          grid: { color: 'rgba(0, 0, 0, 0.05)' },
          ticks: { color: chartTheme.color, font: chartTheme.font },
          title: { display: true, text: 'External Characteristics (EC) Context Score', color: chartTheme.color, font: { size: 10 } }
        }
      }
    }
  });
}

/**
 * 3. Department Risk Breakdown
 */
function initDeptRiskChart() {
  const ctx = document.getElementById('deptRiskChart');
  if (!ctx) return;

  if (charts.deptRisk) charts.deptRisk.destroy();

  const labels = CAMPUS_ANALYTICS.departmentBreakdown.map(d => d.department);
  const highData = CAMPUS_ANALYTICS.departmentBreakdown.map(d => d.high);
  const medData = CAMPUS_ANALYTICS.departmentBreakdown.map(d => d.medium);
  const lowData = CAMPUS_ANALYTICS.departmentBreakdown.map(d => d.low);

  charts.deptRisk = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        { label: 'Critical Risk', data: highData, backgroundColor: '#000000', borderRadius: 4 },
        { label: 'Moderate Risk', data: medData, backgroundColor: '#6B7280', borderRadius: 4 },
        { label: 'On Track', data: lowData, backgroundColor: '#D1D5DB', borderRadius: 4 }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'top', labels: { color: chartTheme.color, font: chartTheme.font, usePointStyle: true } }
      },
      scales: {
        x: {
          stacked: true,
          grid: { display: false },
          ticks: { color: chartTheme.color, font: chartTheme.font }
        },
        y: {
          stacked: true,
          grid: { color: 'rgba(0, 0, 0, 0.05)' },
          ticks: { color: chartTheme.color, font: chartTheme.font }
        }
      }
    }
  });
}

/**
 * 4. Student SRL Habit Tracker Bar Chart
 */
function initSrlHabitChart() {
  const ctx = document.getElementById('srlHabitChart');
  if (!ctx) return;

  if (charts.srlHabit) charts.srlHabit.destroy();

  charts.srlHabit = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      datasets: [
        {
          label: 'Logged Study Hours',
          data: [1.8, 2.4, 0.5, 3.2, 1.2, 2.8, 1.5],
          backgroundColor: '#000000',
          borderRadius: 4
        },
        {
          label: 'Target Cohort Baseline',
          data: [2.0, 2.0, 2.0, 2.0, 2.0, 2.5, 2.5],
          backgroundColor: '#D1D5DB',
          borderRadius: 4
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'top', labels: { color: chartTheme.color, font: chartTheme.font, usePointStyle: true } }
      },
      scales: {
        x: { grid: { display: false }, ticks: { color: chartTheme.color, font: chartTheme.font } },
        y: {
          grid: { color: 'rgba(0, 0, 0, 0.05)' },
          ticks: { color: chartTheme.color, font: chartTheme.font, callback: (v) => v + 'h' }
        }
      }
    }
  });
}

/**
 * 5. Student Deep-Dive Radar Chart
 */
function renderStudentRadarChart(student) {
  const ctx = document.getElementById('studentRadarChart');
  if (!ctx) return;

  if (charts.studentRadar) charts.studentRadar.destroy();

  charts.studentRadar = new Chart(ctx, {
    type: 'radar',
    data: {
      labels: ['Academic (CGPA)', 'VLE Hours', 'Quiz Completion', 'Attendance', 'Assignment On-Time', 'Discussion'],
      datasets: [
        {
          label: student.name,
          data: [
            (student.cgpa / 10) * 100,
            Math.min(100, (student.vleStudyHoursWeekly / 12) * 100),
            student.quizCompletionRate,
            student.attendanceRate,
            Math.max(20, 100 - (student.assignmentLatenessDays * 15)),
            Math.min(100, student.forumPosts * 12)
          ],
          borderColor: '#000000',
          backgroundColor: 'rgba(0, 0, 0, 0.12)',
          borderWidth: 2,
          pointBackgroundColor: '#000000'
        },
        {
          label: 'Class Average',
          data: [75, 65, 78, 85, 80, 50],
          borderColor: '#9CA3AF',
          backgroundColor: 'rgba(0, 0, 0, 0.03)',
          borderWidth: 1.5,
          borderDash: [4, 4]
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'bottom', labels: { color: chartTheme.color, font: chartTheme.font } }
      },
      scales: {
        r: {
          angleLines: { color: 'rgba(0, 0, 0, 0.08)' },
          grid: { color: 'rgba(0, 0, 0, 0.08)' },
          pointLabels: { color: '#111827', font: { size: 10, weight: '600' } },
          ticks: { display: false, max: 100, min: 0 }
        }
      }
    }
  });
}
