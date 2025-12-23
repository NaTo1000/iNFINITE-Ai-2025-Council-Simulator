# Configuration Management

## Overview
Centralized configuration management for the Council Simulator to ensure consistent, reliable, and maintainable system configuration.

## Configuration Principles

### 1. Separation of Concerns
- Separate configuration from code
- Environment-specific configs
- Sensitive data isolated
- Version controlled (except secrets)

### 2. DRY (Don't Repeat Yourself)
- Shared configurations
- Template-based configs
- Inheritance where appropriate
- Default values defined

### 3. Security First
- Secrets not in version control
- Encryption at rest
- Access controls
- Audit logging

### 4. Documentation
- All configs documented
- Change history maintained
- Examples provided
- Validation rules specified

## Configuration Structure

```
config/
├── default.json          # Default configuration
├── development.json      # Development overrides
├── staging.json         # Staging overrides
├── production.json      # Production overrides
├── test.json           # Test environment
├── schemas/            # JSON schemas for validation
│   ├── protocol.schema.json
│   ├── pipeline.schema.json
│   └── dashboard.schema.json
├── examples/           # Example configurations
│   └── custom-protocol.json
└── secrets/            # Secret management (not in git)
    └── .gitignore     # Ensures secrets not committed
```

## Configuration Categories

### System Configuration
```json
{
  "system": {
    "name": "iNFINITE-AI-Council-Simulator",
    "version": "1.0.0",
    "environment": "production",
    "logLevel": "info",
    "timezone": "UTC"
  }
}
```

### Protocol Configuration
```json
{
  "protocols": {
    "decisionMaking": {
      "enabled": true,
      "timeoutMs": 5000,
      "consensusThreshold": 0.66,
      "maxRetries": 3
    },
    "dataValidation": {
      "enabled": true,
      "strictMode": true,
      "qualityThreshold": 0.75
    }
  }
}
```

### Data Integration Configuration
```json
{
  "dataIntegration": {
    "pipeline": {
      "batchSize": 100,
      "workers": 4,
      "retryAttempts": 3,
      "retryDelayMs": 1000
    },
    "sources": {
      "researchLogs": {
        "path": "/research/logs",
        "pollIntervalMs": 60000
      },
      "conferenceResults": {
        "path": "/research/conference",
        "pollIntervalMs": 3600000
      }
    },
    "quality": {
      "minCompletenessScore": 0.95,
      "minAccuracyScore": 0.90,
      "alertThreshold": 0.75
    }
  }
}
```

### Dashboard Configuration
```json
{
  "dashboard": {
    "refreshRates": {
      "executiveSummary": 300000,
      "protocolPerformance": 60000,
      "researchActivity": 3600000
    },
    "metrics": {
      "retentionDays": 90,
      "aggregationInterval": "1m"
    },
    "alerts": {
      "enabled": true,
      "channels": ["email", "slack"]
    }
  }
}
```

### Continuous Improvement Configuration
```json
{
  "continuousImprovement": {
    "reviews": {
      "scheduleEnabled": true,
      "weeklyReview": "Monday 10:00",
      "monthlyReview": "First Monday 14:00"
    },
    "forkManagement": {
      "autoCleanup": true,
      "staleAfterDays": 90,
      "requireTests": true
    },
    "bugTracking": {
      "slaHours": {
        "critical": 4,
        "high": 24,
        "medium": 168,
        "low": 720
      }
    }
  }
}
```

## Environment-Specific Configuration

### Development
```json
{
  "system": {
    "environment": "development",
    "logLevel": "debug"
  },
  "protocols": {
    "decisionMaking": {
      "timeoutMs": 30000
    }
  },
  "dataIntegration": {
    "pipeline": {
      "workers": 1
    }
  }
}
```

### Production
```json
{
  "system": {
    "environment": "production",
    "logLevel": "warn"
  },
  "protocols": {
    "decisionMaking": {
      "timeoutMs": 5000
    }
  },
  "dataIntegration": {
    "pipeline": {
      "workers": 8
    }
  }
}
```

## Secret Management

### Secret Categories
1. **API Keys**: External service authentication
2. **Database Credentials**: Database access
3. **Encryption Keys**: Data encryption
4. **Service Tokens**: Inter-service auth
5. **Certificates**: SSL/TLS certificates

### Secret Storage Options

#### Development
- Local `.env` file (gitignored)
- Environment variables
- Local secret store

#### Production
- Cloud secret managers (AWS Secrets Manager, Azure Key Vault)
- HashiCorp Vault
- Kubernetes Secrets
- Encrypted configuration files

### Secret Access Pattern
```javascript
// Example: Loading secrets securely
const secrets = {
  databasePassword: process.env.DB_PASSWORD || 
                    loadFromVault('database/password'),
  apiKey: process.env.API_KEY || 
          loadFromVault('api/key')
};

// Never log secrets
logger.info('Database connected', { user: dbUser }); // OK
logger.info('Password:', password); // NEVER DO THIS
```

## Configuration Validation

### JSON Schema Validation
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "protocols": {
      "type": "object",
      "properties": {
        "decisionMaking": {
          "type": "object",
          "properties": {
            "timeoutMs": {
              "type": "integer",
              "minimum": 1000,
              "maximum": 60000
            },
            "consensusThreshold": {
              "type": "number",
              "minimum": 0.5,
              "maximum": 1.0
            }
          },
          "required": ["timeoutMs", "consensusThreshold"]
        }
      }
    }
  }
}
```

### Validation on Startup
```javascript
// Example: Validate configuration on startup
const Ajv = require('ajv');
const ajv = new Ajv();

function validateConfig(config, schema) {
  const validate = ajv.compile(schema);
  const valid = validate(config);
  
  if (!valid) {
    console.error('Configuration validation failed:');
    console.error(validate.errors);
    process.exit(1);
  }
  
  return config;
}

// Load and validate
const config = loadConfig();
const schema = loadSchema();
const validatedConfig = validateConfig(config, schema);
```

## Configuration Loading

### Priority Order
1. Command-line arguments (highest priority)
2. Environment variables
3. Environment-specific config file
4. Default config file (lowest priority)

### Loading Example
```javascript
// Example: Configuration loader
function loadConfiguration() {
  // 1. Load defaults
  const defaults = require('./config/default.json');
  
  // 2. Load environment-specific
  const env = process.env.NODE_ENV || 'development';
  const envConfig = require(`./config/${env}.json`);
  
  // 3. Merge configurations
  const config = merge(defaults, envConfig);
  
  // 4. Override with environment variables
  applyEnvironmentOverrides(config);
  
  // 5. Override with CLI args
  applyCLIOverrides(config);
  
  // 6. Validate
  validateConfiguration(config);
  
  return config;
}
```

## Dynamic Configuration

### Hot Reloading
```javascript
// Example: Watch for config changes
const fs = require('fs');

function watchConfiguration(configPath, callback) {
  fs.watch(configPath, (eventType, filename) => {
    if (eventType === 'change') {
      console.log(`Configuration changed: ${filename}`);
      
      // Reload and validate
      const newConfig = loadConfiguration();
      
      // Apply new configuration
      callback(newConfig);
    }
  });
}
```

### Feature Flags
```json
{
  "featureFlags": {
    "newProtocolEngine": {
      "enabled": false,
      "rolloutPercentage": 0
    },
    "mlDecisionSupport": {
      "enabled": true,
      "rolloutPercentage": 25
    }
  }
}
```

## Configuration Management Tools

### Version Control
- All configs in Git (except secrets)
- Meaningful commit messages
- Review changes like code
- Tag releases

### Configuration as Code
```yaml
# Example: Terraform configuration
resource "aws_secretsmanager_secret" "db_password" {
  name = "council-simulator/db-password"
  
  tags = {
    Environment = "production"
    ManagedBy   = "terraform"
  }
}
```

### Documentation
- README for each config
- Inline comments
- Change log
- Migration guides

## Best Practices

### Do's
- ✓ Use environment variables for secrets
- ✓ Validate configurations on startup
- ✓ Document all configuration options
- ✓ Use sensible defaults
- ✓ Version control non-secret configs
- ✓ Test configuration changes
- ✓ Monitor configuration usage

### Don'ts
- ✗ Hardcode secrets in code
- ✗ Commit secrets to version control
- ✗ Use production config in development
- ✗ Skip validation
- ✗ Make configs overly complex
- ✗ Change configs without testing
- ✗ Share secrets insecurely

## Configuration Auditing

### Audit Log
Track configuration changes:
- Who made the change
- What was changed
- When it was changed
- Why (from commit message)
- Impact assessment

### Configuration Drift
Monitor for unauthorized changes:
- Compare against known good state
- Alert on unexpected changes
- Automated remediation
- Regular audits

## Troubleshooting

### Common Issues

#### Missing Configuration
```
Error: Configuration key 'protocols.decisionMaking.timeout' not found

Solution:
1. Check configuration file exists
2. Verify key spelling
3. Ensure defaults are set
4. Check environment overrides
```

#### Invalid Configuration
```
Error: Configuration validation failed: 
  consensusThreshold must be between 0.5 and 1.0

Solution:
1. Review configuration value
2. Check schema requirements
3. Validate against examples
4. Run validation tool
```

#### Secret Access Failure
```
Error: Unable to retrieve secret 'db-password'

Solution:
1. Verify secret exists in store
2. Check access permissions
3. Validate authentication
4. Check network connectivity
```

## Maintenance

### Regular Tasks
- **Weekly**: Review configuration changes
- **Monthly**: Audit secret access
- **Quarterly**: Update defaults, cleanup unused configs

### Configuration Review Checklist
- [ ] All configs documented
- [ ] Schemas up to date
- [ ] No secrets in version control
- [ ] Validation working
- [ ] Environment-specific configs correct
- [ ] Defaults sensible
- [ ] Examples provided

## Conclusion
Proper configuration management ensures system consistency, security, and maintainability. By following these guidelines, we maintain reliable configuration across all environments while protecting sensitive information.
