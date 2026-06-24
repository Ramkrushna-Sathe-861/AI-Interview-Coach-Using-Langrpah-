import React from 'react'

const AGENTS = [
  { step: '1', title: 'Resume Agent', description: 'Extracts & understands your resume', status: 'Completed' },
  { step: '2', title: 'Skill Gap Agent', description: 'Compares skills with target role', status: 'Completed' },
  { step: '3', title: 'Learning Agent', description: 'Creates a personalized roadmap', status: 'Completed' },
  { step: '4', title: 'Interview Agent', description: 'Conducts adaptive mock interviews', status: 'In Progress' },
  { step: '5', title: 'Feedback Agent', description: 'Analyzes performance & gives feedback', status: 'Pending' },
]

export default function Dashboard(): JSX.Element {
  return (
    <main className="dashboard-grid">
      <section className="dashboard-left">
        <div className="hero-card card">
          <div className="hero-copy">
            <div className="hero-label">AI COACH</div>
            <h1>Welcome back, Aman! 👋</h1>
            <p className="hero-text">
              Let’s continue your interview preparation journey with personalized guidance,
              practice, and analytics from your AI-powered agent team.
            </p>
            <div className="hero-actions">
              <button className="btn hero-btn">View Agent Pipeline</button>
              <button className="btn secondary hero-btn">Upload Resume</button>
            </div>
          </div>
          <div className="hero-visual">
            <div className="robot-banner">
              <div className="robot-icon">🤖</div>
              <div className="robot-glow" />
              <div className="robot-panel">
                <div>AI Interview Coach</div>
              </div>
            </div>
          </div>
        </div>

        <div className="pipeline-card card">
          <div className="panel-head">
            <div>
              <h2>Agent Pipeline</h2>
              <p className="meta">See how our 5 AI agents work together for your success.</p>
            </div>
            <a className="panel-link" href="#">See details →</a>
          </div>
          <div className="pipeline-list">
            {AGENTS.map((agent) => (
              <div key={agent.step} className={`pipeline-step ${agent.status === 'In Progress' ? 'active' : ''}`}>
                <div className="step-badge">{agent.step}</div>
                <div>
                  <h3>{agent.title}</h3>
                  <p className="meta">{agent.description}</p>
                </div>
                <span className={`status-pill ${agent.status === 'Completed' ? 'complete' : agent.status === 'In Progress' ? 'progress' : 'pending'}`}>
                  {agent.status}
                </span>
              </div>
            ))}
          </div>
        </div>

        <div className="stats-grid">
          <article className="stat-card card">
            <div className="stat-head">
              <h3>Skill Match Overview</h3>
              <span className="badge soft">78% Match Score</span>
            </div>
            <div className="stat-ring">78%</div>
            <div className="stat-list">
              <div><span className="dot green" /> Strong Skills <strong>18</strong></div>
              <div><span className="dot blue" /> Matched Skills <strong>24</strong></div>
              <div><span className="dot red" /> Missing Skills <strong>6</strong></div>
            </div>
            <a className="panel-link" href="#">View Full Analysis →</a>
          </article>

          <article className="stat-card card">
            <div className="stat-head">
              <h3>Learning Progress</h3>
              <span className="meta">This Week</span>
            </div>
            <div className="progress-block">
              <div className="progress-score">65%</div>
              <div className="progress-bar"><div style={{ width: '65%' }} /></div>
            </div>
            <div className="progress-meta">
              <span>Completed 12</span>
              <span>In Progress 8</span>
              <span>Remaining 6</span>
            </div>
            <a className="panel-link" href="#">Go to Roadmap →</a>
          </article>

          <article className="stat-card card">
            <div className="stat-head">
              <h3>Interview Insights</h3>
              <span className="meta">This Month</span>
            </div>
            <div className="insight-grid">
              <div>
                <div className="insight-value">08</div>
                <div className="meta">Interviews Taken</div>
              </div>
              <div>
                <div className="insight-value">8.2/10</div>
                <div className="meta">Average Score</div>
              </div>
            </div>
            <div className="insight-stats">
              <span className="positive">+33%</span>
              <span className="positive">+12%</span>
            </div>
            <a className="panel-link" href="#">View All Interviews →</a>
          </article>
        </div>

        <div className="wide-grid">
          <article className="activity-card card">
            <div className="panel-head">
              <h3>Recent Activity</h3>
              <a className="panel-link" href="#">View All</a>
            </div>
            <ul className="activity-list">
              <li>
                <div className="activity-dot completed" />
                <div>
                  <strong>Mock Interview Completed</strong>
                  <p className="meta">System Design Interview - 1 hour ago</p>
                </div>
                <span className="tag">8.5/10</span>
              </li>
              <li>
                <div className="activity-dot"> </div>
                <div>
                  <strong>New Learning Module Completed</strong>
                  <p className="meta">Vector Databases Basics - 3 hours ago</p>
                </div>
                <span className="tag">Completed</span>
              </li>
              <li>
                <div className="activity-dot"> </div>
                <div>
                  <strong>Resume Analyzed</strong>
                  <p className="meta">Software Engineer Resume.pdf - 1 day ago</p>
                </div>
                <span className="tag">View</span>
              </li>
            </ul>
          </article>

          <article className="activity-card card">
            <div className="panel-head">
              <h3>Upcoming Interview</h3>
              <a className="panel-link" href="#">View All</a>
            </div>
            <div className="upcoming-event">
              <div>
                <div className="event-date">24 May</div>
                <div className="event-title">System Design Interview</div>
                <div className="meta">Google • Senior Backend Engineer</div>
                <div className="meta">10:00 AM - 11:00 AM</div>
              </div>
              <button className="btn">Start Practice</button>
            </div>
            <div className="quick-actions">
              <button className="action-item">Upload Resume</button>
              <button className="action-item">Start Interview</button>
              <button className="action-item">Practice Questions</button>
              <button className="action-item">Explore Roadmap</button>
            </div>
          </article>
        </div>
      </section>

      <aside className="dashboard-right">
        <div className="progress-card card">
          <div className="panel-head">
            <h3>Overall Progress</h3>
            <span className="badge soft">This Week</span>
          </div>
          <div className="progress-ring">76%</div>
          <div className="progress-summary">
            <div>
              <strong>245</strong>
              <p className="meta">Questions Practiced</p>
            </div>
            <div>
              <strong>12</strong>
              <p className="meta">Mock Interviews</p>
            </div>
            <div>
              <strong>7 Days</strong>
              <p className="meta">Current Streak</p>
            </div>
          </div>
          <a className="panel-link" href="#">View Detailed Analytics →</a>
        </div>

        <div className="insight-panel card">
          <div className="insight-head">
            <h3>Strengths</h3>
            <a className="panel-link" href="#">View All</a>
          </div>
          <div className="skill-bar"><span style={{ width: '90%' }} /></div>
          <div className="skill-item"><span>Python</span><strong>90%</strong></div>
          <div className="skill-bar"><span style={{ width: '85%' }} /></div>
          <div className="skill-item"><span>FastAPI</span><strong>85%</strong></div>
          <div className="skill-bar"><span style={{ width: '80%' }} /></div>
          <div className="skill-item"><span>SQL</span><strong>80%</strong></div>
          <div className="skill-bar"><span style={{ width: '75%' }} /></div>
          <div className="skill-item"><span>System Design</span><strong>75%</strong></div>
        </div>

        <div className="insight-panel card">
          <div className="insight-head">
            <h3>Weak Areas</h3>
            <a className="panel-link" href="#">View All</a>
          </div>
          <div className="skill-bar danger"><span style={{ width: '40%' }} /></div>
          <div className="skill-item"><span>Kubernetes</span><strong>40%</strong></div>
          <div className="skill-bar danger"><span style={{ width: '45%' }} /></div>
          <div className="skill-item"><span>Docker</span><strong>45%</strong></div>
          <div className="skill-bar danger"><span style={{ width: '50%' }} /></div>
          <div className="skill-item"><span>AWS</span><strong>50%</strong></div>
          <div className="skill-bar danger"><span style={{ width: '55%' }} /></div>
          <div className="skill-item"><span>CI/CD</span><strong>55%</strong></div>
        </div>
      </aside>
    </main>
  )
}
