
import os

path = r"c:\Users\lokan\OneDrive\Desktop\mejor Project -Render\templates\citizen\apply_form_bootstrap.html"

content = """{% extends 'base_bootstrap.html' %}
{% block sidebar_mobile %}
<div class="mb-4">
    <div class="text-uppercase text-muted fw-black mb-2 tracking-widest" style="font-size: 10px;">Citizen Hub</div>
    <nav class="nav flex-column gap-1">
        <a class="nav-link rounded-3 d-flex align-items-center gap-3 py-3" href="{% url 'citizen:dashboard' %}">
            <i class="bi bi-speedometer2 text-primary"></i> <span>Dashboard</span>
        </a>
        <a class="nav-link rounded-3 d-flex align-items-center gap-3 py-3 active" href="{% url 'citizen:services' %}">
            <i class="bi bi-grid-fill text-primary"></i> <span>Service Portal</span>
        </a>
        <a class="nav-link rounded-3 d-flex align-items-center gap-3 py-3" href="{% url 'citizen:locker' %}">
            <i class="bi bi-safe2 text-primary"></i> <span>Digital Locker</span>
        </a>
        <a class="nav-link rounded-3 d-flex align-items-center gap-3 py-3" href="{% url 'citizen:grievances' %}">
            <i class="bi bi-megaphone text-primary"></i> <span>Grievance Box</span>
        </a>
        <a class="nav-link rounded-3 d-flex align-items-center gap-3 py-3" href="{% url 'citizen:appointments' %}">
            <i class="bi bi-calendar-event text-primary"></i> <span>My Visits</span>
        </a>
    </nav>
</div>
<div class="border-top my-3"></div>
{% endblock %}

{% block title %}Apply for {{ service.service_name }} | e-Gov Portal{% endblock %}

{% block content %}
<div class="container-fluid bg-light min-vh-100 py-4">
    <div class="container">
        <!-- Header -->
        <div class="row mb-4">
            <div class="col-md-8">
                <h2 class="mb-2">Apply for {{ service.service_name }}</h2>
                <p class="text-muted">
                    <i class="bi bi-building"></i> {{ service.department.department_name }} •
                    <i class="bi bi-clock"></i> {{ service.processing_days }} Days Processing Time
                </p>
            </div>
            <div class="col-md-4 text-md-end">
                <a href="{% url 'citizen:services' %}" class="btn btn-outline-secondary">
                    <i class="bi bi-arrow-left"></i> Back to Services
                </a>
            </div>
        </div>

        <div class="row">
            <!-- Main Form Card -->
            <div class="col-lg-8">
                <div class="card shadow-sm">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0"><i class="bi bi-file-earmark-plus"></i> Application Form</h5>
                    </div>
                    <div class="card-body">
                        <form method="POST" enctype="multipart/form-data">
                            {% csrf_token %}

                            <!-- Priority Selection (Required) -->
                            <div class="mb-4">
                                <label class="form-label fw-bold">
                                    Application Priority <span class="text-danger">*</span>
                                </label>
                                <div class="row g-3">
                                    <div class="col-md-4">
                                        <div class="form-check card p-3 h-100">
                                            <input class="form-check-input" type="radio" name="priority" value="normal"
                                                id="priorityNormal" {% if not existing_app or existing_app.priority == "normal" %}checked{% endif %}>
                                            <label class="form-check-label w-100" for="priorityNormal">
                                                <div class="d-flex align-items-center">
                                                    <i class="bi bi-circle-fill text-secondary fs-4 me-2"></i>
                                                    <div>
                                                        <strong>Normal</strong>
                                                        <p class="small text-muted mb-0">Standard processing time</p>
                                                    </div>
                                                </div>
                                            </label>
                                        </div>
                                    </div>
                                    <div class="col-md-4">
                                        <div class="form-check card p-3 h-100 border-warning">
                                            <input class="form-check-input" type="radio" name="priority"
                                                value="emergency" id="priorityEmergency" {% if existing_app.priority == "emergency" %}checked{% endif %}>
                                            <label class="form-check-label w-100" for="priorityEmergency">
                                                <div class="d-flex align-items-center">
                                                    <i
                                                        class="bi bi-exclamation-triangle-fill text-warning fs-4 me-2"></i>
                                                    <div>
                                                        <strong>Emergency</strong>
                                                        <p class="small text-muted mb-0">Expedited processing</p>
                                                    </div>
                                                </div>
                                            </label>
                                        </div>
                                    </div>
                                    <div class="col-md-4">
                                        <div class="form-check card p-3 h-100 border-danger">
                                            <input class="form-check-input" type="radio" name="priority"
                                                value="disaster" id="priorityDisaster" {% if existing_app.priority == "disaster" %}checked{% endif %}>
                                            <label class="form-check-label w-100" for="priorityDisaster">
                                                <div class="d-flex align-items-center">
                                                    <i class="bi bi-lightning-fill text-danger fs-4 me-2"></i>
                                                    <div>
                                                        <strong>Disaster</strong>
                                                        <p class="small text-muted mb-0">Immediate attention</p>
                                                    </div>
                                                </div>
                                            </label>
                                        </div>
                                    </div>
                                </div>
                                <small class="form-text text-muted">
                                    Select priority level based on urgency. Disaster/Emergency requires valid
                                    justification.
                                </small>
                            </div>

                            <!-- Remarks -->
                            <div class="mb-4">
                                <label for="remarks" class="form-label fw-bold">Additional Remarks</label>
                                <textarea class="form-control" id="remarks" name="remarks" rows="4"
                                    placeholder="Provide any additional information or special circumstances...">{{ existing_app.remarks|default:"" }}</textarea>
                            </div>

                            <!-- Document Upload Section -->
                            <div class="mb-4">
                                <label class="form-label fw-bold">Upload Documents (Optional)</label>
                                <div class="card bg-light border-2 border-dashed">
                                    <div class="card-body">
                                        <div class="row g-3">
                                            <div class="col-md-6">
                                                <label for="docType" class="form-label small">Document Type</label>
                                                <input type="text" class="form-control" id="docType"
                                                    name="document_type" placeholder="e.g., ID Proof, Address Proof">
                                            </div>
                                            <div class="col-md-6">
                                                <label for="docFile" class="form-label small">Select File (PDF/JPG/PNG,
                                                    max 5MB)</label>
                                                <input type="file" class="form-control" id="docFile" name="file_path"
                                                    accept=".pdf,.jpg,.jpeg,.png">
                                            </div>
                                        </div>
                                        <div class="mt-2">
                                            <small class="text-muted">
                                                <i class="bi bi-info-circle"></i> Supported formats: PDF, JPG, PNG | Max
                                                size: 5MB
                                            </small>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Declaration -->
                            <div class="mb-4">
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox" id="declaration" required>
                                    <label class="form-check-label" for="declaration">
                                        I hereby declare that the information provided is true and correct to the best
                                        of my knowledge.
                                        I understand that providing false information may result in rejection of my
                                        application.
                                    </label>
                                </div>
                            </div>

                            <!-- Submit Buttons -->
                            <div class="d-grid gap-2 d-md-flex justify-content-md-end align-items-center">
                                <a href="{% url 'citizen:services' %}" class="btn btn-outline-secondary">
                                    Cancel
                                </a>
                                <button type="submit" name="action" value="draft" class="btn btn-outline-primary"
                                    formnovalidate>
                                    <i class="bi bi-save"></i> Save as Draft
                                </button>
                                <button type="submit" name="action" value="submit" class="btn btn-primary btn-lg">
                                    <i class="bi bi-send"></i> Submit Application
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>

            <!-- Info Sidebar -->
            <div class="col-lg-4">
                <!-- Service Information -->
                <div class="card shadow-sm mb-3">
                    <div class="card-header bg-info text-white">
                        <h6 class="mb-0"><i class="bi bi-info-circle"></i> Service Information</h6>
                    </div>
                    <div class="card-body">
                        <ul class="list-unstyled mb-0">
                            <li class="mb-2">
                                <i class="bi bi-building text-primary"></i>
                                <strong>Department:</strong><br>
                                <span class="text-muted">{{ service.department.department_name }}</span>
                            </li>
                            <li class="mb-2">
                                <i class="bi bi-clock text-primary"></i>
                                <strong>Processing Time:</strong><br>
                                <span class="text-muted">{{ service.processing_days }} Working Days</span>
                            </li>
                            <li class="mb-2">
                                <i class="bi bi-currency-rupee text-primary"></i>
                                <strong>Service Fee:</strong><br>
                                <span class="text-muted">{% if service.fee_amount > 0 %}₹{{ service.fee_amount }}{% else %}Free{% endif %}</span>
                            </li>
                        </ul>
                    </div>
                </div>

                <!-- Required Documents -->
                <div class="card shadow-sm mb-3">
                    <div class="card-header bg-warning text-dark">
                        <h6 class="mb-0"><i class="bi bi-file-earmark-check"></i> Required Documents</h6>
                    </div>
                    <div class="card-body">
                        <p class="small text-muted">{{ service.required_documents }}</p>
                        <div class="alert alert-light border mb-0">
                            <small>
                                <i class="bi bi-lightbulb"></i> <strong>Tip:</strong> Keep all documents ready before
                                starting the application.
                            </small>
                        </div>
                    </div>
                </div>

                <!-- Help Card -->
                <div class="card shadow-sm">
                    <div class="card-body text-center">
                        <i class="bi bi-question-circle text-primary fs-1 mb-2"></i>
                        <h6>Need Help?</h6>
                        <p class="small text-muted">Contact our support team</p>
                        <a href="{% url 'core:contact' %}" class="btn btn-sm btn-outline-primary">
                            <i class="bi bi-envelope"></i> Contact Support
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
    .form-check.card {
        cursor: pointer;
        transition: all 0.2s;
    }

    .form-check.card:hover {
        background-color: #f8f9fa;
    }

    .form-check-input:checked+.form-check-label {
        font-weight: bold;
    }
</style>
{% endblock %}"""

try:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully wrote full content.")
except Exception as e:
    print(f"Error: {e}")
