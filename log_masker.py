import re
from typing import Dict


class LogMasker:
    def __init__(self):
        self.email_mapping: Dict[str, str] = {}
        self.ip_mapping: Dict[str, str] = {}
        self.counter = 1

    def _generate_mask(self, prefix: str) -> str:
        """Generate a unique mask for sensitive data."""
        mask = f"{prefix}-{self.counter:02d}"
        self.counter += 1
        return mask

    def _mask_email(self, email: str) -> str:
        """Mask an email address and maintain the mapping."""
        email = email.group()
        if email not in self.email_mapping:
            self.email_mapping[email] = self._generate_mask("USER")
        return self.email_mapping[email]

    def _mask_ip(self, ip: str) -> str:
        """Mask an IP address and maintain the mapping."""
        ip = ip.group()
        if ip not in self.ip_mapping:
            self.ip_mapping[ip] = self._generate_mask("IP")
        return self.ip_mapping[ip]

    def mask_log_entry(self, log_entry: str) -> str:
        """Mask sensitive information in a log entry."""
        # Regular expressions for matching emails and IPs
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'

        # Replace emails
        masked_entry = re.sub(email_pattern, lambda m: self._mask_email(m), log_entry)
        
        # Replace IPs
        masked_entry = re.sub(ip_pattern, lambda m: self._mask_ip(m), masked_entry)
        
        return masked_entry

    def unmask_log_entry(self, masked_entry: str) -> str:
        """Unmask sensitive information in a log entry."""
        # Create reverse mappings
        email_reverse = {v: k for k, v in self.email_mapping.items()}
        ip_reverse = {v: k for k, v in self.ip_mapping.items()}
        # print(email_reverse)
        # print(ip_reverse)
        # Replace masked values with original values
        unmasked_entry = masked_entry
        for mask, email in email_reverse.items():
            unmasked_entry = unmasked_entry.replace(mask, email)
        for mask, ip in ip_reverse.items():
            unmasked_entry = unmasked_entry.replace(mask, ip)
        
        return unmasked_entry

