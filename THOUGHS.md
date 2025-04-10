# Assumptions

1. This Tech Lead position included in 6-person team
2. Prior to conversations with Saara & Oskari
    - The Team Lead position heavily focus on back-end side
    - There are 3 front-end developer (1 lead, 2 senior) and 2 sernior back-end developer
3. TalentAdore serves services in global scale

# Team Responsibilities to Implement 

Each developer of the back-end and front-end teams rotates between services on a 2-sprint basis. This rotation ensures everyone understands all services, preventing knowledge gaps.

## Backend Team:
- **Tech Lead**: Architecture design, API gateway setup, code reviews, Organization service development & testing, and technical decisions
- **Backend Dev 1**: Feedback service development and testing
- **Backend Dev 2**: Member service development and testing

## Frontend Team:
- **Frontend Lead**: Component library design, shared components, state management setup, code reviews, and Organization views
- **Frontend Dev 1**: Feedback management views
- **Frontend Dev 2**: Member management views

# Scaling to Millions of Records

To handle millions of records efficiently, I would suggest these implementations:

1. **Database Optimization**:
    - Leverage partitioning for large tables
    - Add database indexing for high-frequency queried fields and large-distinct-value columns
    - Implement pagination for all GET endpoints

2. **Caching**:
    - Add Redis caching for frequently accessed data
    - Implement cache invalidation strategies

3. **Infrastructure**:
    - Implement Terraform
    - Use K8s for easier scaling out
    - Set up auto-scaling based on traffic patterns
    - Pre-scale before any big event with huge traffic
    - Move static files to CDN (based on assumption 3)

4. **Monitoring**:
   - Monitor performance metrics in Grafana/Prometheus, Azure Insights (or AWS equivalents)
   - Set up alerts for slow queries or high resource usage
   - Slack integration for quick actions

# Long-term Maintainability

To ensure the codebase remains maintainable as it grows:

1. **Code Organization**:
    - Seperate microservices and its components
    - Standardize API patterns across services
    - Shared libraries for common functionality

2. **Documentation**:
    - Maintain comprehensive API documentation
    - Document architectural decisions
    - Create onboarding guides for new developers

3. **Testing**:
    - Write unit test before developing
    - Maintain high test coverage (unit, integration, E2E)
    - Automate testing with Github Action, Gitlab CI/CD, ...
    - Regular performance testing

4. **Development Processes**:
    - 2-approval code review for all changes
    - Follow Coding principles such as DRY, KISS, ...
    - Apply appropriate design patterns during developement
    - Regular dependency updates
    - Technical sharing every sprint

5. **Monitoring**:
    - Comprehensive logging strategy
    - Centralized error tracking