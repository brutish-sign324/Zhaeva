#!/usr/bin/env python3
import os
import socket
import tqdm
import sys
import threading
import time
import hashlib
import json
import pickle
import zlib
import ssl
import logging
from datetime import datetime
import argparse
import queue
import signal
import tempfile
import shutil
import stat
import math
import collections
import struct
import secrets
import base64
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, asdict, field
from enum import Enum, auto
from concurrent.futures import ThreadPoolExecutor, Future, as_completed

# ============================================================
#  ANIMATION & COLOR SYSTEM
# ============================================================

class CyberColors:
    """Cyber-themed color system for terminal output"""
    
    # ANSI color codes
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    HIDDEN = '\033[8m'
    
    # Foreground colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
    # Cyber theme colors
    NEON_GREEN = '\033[38;2;0;255;200m'
    NEON_BLUE = '\033[38;2;0;150;255m'
    NEON_PURPLE = '\033[38;2;150;0;255m'
    NEON_PINK = '\033[38;2;255;0;150m'
    NEON_ORANGE = '\033[38;2;255;150;0m'
    NEON_RED = '\033[38;2;255;0;50m'
    NEON_CYAN = '\033[38;2;0;255;255m'
    NEON_YELLOW = '\033[38;2;255;255;0m'
    
    @staticmethod
    def gradient_text(text: str, start_color: str, end_color: str) -> str:
        """Create a gradient color effect for text"""
        return f"{start_color}{text}{CyberColors.RESET}"
    
    @staticmethod
    def cyber_frame(text: str, color: str = NEON_BLUE) -> str:
        """Wrap text in a cyber-style frame"""
        lines = text.split('\n')
        width = max(len(line) for line in lines) + 4
        top = f"╔{'═' * width}╗"
        bottom = f"╚{'═' * width}╝"
        framed = [top]
        for line in lines:
            framed.append(f"║ {line.ljust(width-2)} ║")
        framed.append(bottom)
        return f"{color}{chr(10).join(framed)}{CyberColors.RESET}"

class AnimationEngine:
    """Engine for generating terminal animations"""
    
    @staticmethod
    def loading_spinner(message: str = "Processing", duration: float = 2.0):
        """Display a loading spinner animation"""
        spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        end_time = time.time() + duration
        i = 0
        while time.time() < end_time:
            sys.stdout.write(f'\r{CyberColors.NEON_BLUE}{spinner[i % len(spinner)]}{CyberColors.RESET} {message}... ')
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
        sys.stdout.write('\r' + ' ' * 80 + '\r')
        sys.stdout.flush()
    
    @staticmethod
    def progress_bar(percentage: float, width: int = 50, 
                     filled_char: str = '█', empty_char: str = '░',
                     color: str = CyberColors.NEON_GREEN) -> str:
        """Generate a cyber-style progress bar"""
        filled = int(width * percentage / 100)
        bar = f"{color}{filled_char * filled}{CyberColors.BRIGHT_BLACK}{empty_char * (width - filled)}{CyberColors.RESET}"
        return f"[{bar}] {percentage:.1f}%"
    
    @staticmethod
    def matrix_rain(lines: int = 10, duration: float = 1.0):
        """Simulate matrix rain animation"""
        chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()'
        end_time = time.time() + duration
        positions = [0] * lines
        
        # Save cursor position
        sys.stdout.write('\033[s')
        
        while time.time() < end_time:
            # Clear screen
            sys.stdout.write('\033[2J\033[H')
            
            for i in range(lines):
                line = ''
                for j in range(80):
                    if j < positions[i]:
                        char = secrets.choice(chars)
                        # Random colors for matrix effect
                        color = CyberColors.NEON_GREEN if secrets.randbelow(10) > 2 else CyberColors.NEON_CYAN
                        line += color + char + CyberColors.RESET
                    else:
                        line += ' '
                sys.stdout.write(line + '\n')
                positions[i] = (positions[i] + 1) % 80
            
            sys.stdout.flush()
            time.sleep(0.05)
        
        # Restore cursor position and clear
        sys.stdout.write('\033[2J\033[H')
        sys.stdout.flush()
    
    @staticmethod
    def hack_effect(text: str, color: str = CyberColors.NEON_GREEN):
        """Display text with hacking effect (characters appear one by one)"""
        sys.stdout.write(color)
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.02 + (secrets.randbelow(30) / 1000))
        sys.stdout.write(CyberColors.RESET + '\n')
    
    @staticmethod
    def pulse_animation(message: str, duration: float = 2.0):
        """Pulse animation with brightness variation"""
        end_time = time.time() + duration
        colors = [
            CyberColors.NEON_GREEN,
            CyberColors.NEON_CYAN,
            CyberColors.NEON_BLUE,
            CyberColors.NEON_PURPLE,
            CyberColors.NEON_PINK,
        ]
        i = 0
        while time.time() < end_time:
            sys.stdout.write(f'\r{colors[i % len(colors)]}{message}{CyberColors.RESET}')
            sys.stdout.flush()
            time.sleep(0.15)
            i += 1
        sys.stdout.write('\r' + ' ' * len(message) + '\r')
        sys.stdout.flush()
    
    @staticmethod
    def typewriter_effect(text: str, delay: float = 0.03):
        """Typewriter effect for text"""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        sys.stdout.write('\n')
    
    @staticmethod
    def bouncing_ball(text: str, duration: float = 2.0):
        """Bouncing text animation"""
        width = 60
        end_time = time.time() + duration
        direction = 1
        pos = 0
        
        while time.time() < end_time:
            sys.stdout.write('\r' + ' ' * pos + text + ' ' * (width - pos - len(text)))
            sys.stdout.flush()
            pos += direction
            if pos >= width - len(text) or pos <= 0:
                direction *= -1
            time.sleep(0.03)
        sys.stdout.write('\r' + ' ' * width + '\r')
        sys.stdout.flush()

class CyberBanner:
    """Cyber-style banner generator"""
    
    @staticmethod
    def display_startup_banner():
        """Display the startup banner with animations"""
        os.system('clear' if os.name == 'posix' else 'cls')
        
        banner_lines = [
            f"{CyberColors.NEON_GREEN}",
            "╔══════════════════════════════════════════════════════════════════════════════╗",
            "║                                                                              ║",
            "║   ███████╗██╗  ██╗ █████╗ ███████╗██╗   ██╗ █████╗                         ║",
            "║   ╚══███╔╝██║  ██║██╔══██╗██╔════╝██║   ██║██╔══██╗                        ║",
            "║     ███╔╝ ███████║███████║█████╗  ██║   ██║███████║                        ║",
            "║    ███╔╝  ██╔══██║██╔══██║██╔══╝  ╚██╗ ██╔╝██╔══██║                        ║",
            "║   ███████╗██║  ██║██║  ██║███████╗ ╚████╔╝ ██║  ██║                        ║",
            "║   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝  ╚═══╝  ╚═╝  ╚═╝                        ║",
            "║                                                                              ║",
            f"║{CyberColors.NEON_BLUE}           ╔══════════════════════════════════════════════════╗{CyberColors.NEON_GREEN}              ║",
            f"║{CyberColors.NEON_BLUE}           ║     Z H A E V A   T R A N S F E R   M A T R I X ║{CyberColors.NEON_GREEN}              ║",
            f"║{CyberColors.NEON_BLUE}           ║              Advanced File Transfer System       ║{CyberColors.NEON_GREEN}              ║",
            f"║{CyberColors.NEON_BLUE}           ║                    Version 2.0.0                 ║{CyberColors.NEON_GREEN}              ║",
            f"║{CyberColors.NEON_BLUE}           ╚══════════════════════════════════════════════════╝{CyberColors.NEON_GREEN}              ║",
            "║                                                                              ║",
            f"║{CyberColors.NEON_PURPLE}                    AUTHOR: SYLHETYHACKVENGER{CyberColors.NEON_GREEN}                                ║",
            f"║{CyberColors.NEON_PURPLE}                       (THE-ERROR808){CyberColors.NEON_GREEN}                                        ║",
            "║                                                                              ║",
            f"║{CyberColors.NEON_CYAN}               AUTHOR IS NOT RESPONSIBLE FOR YOUR MISUSE{CyberColors.NEON_GREEN}                         ║",
            f"║{CyberColors.NEON_CYAN}               • Adaptive Flow Control{CyberColors.NEON_GREEN}                                       ║",
            f"║{CyberColors.NEON_CYAN}               • Multi-Layer Encryption{CyberColors.NEON_GREEN}                                      ║",
            f"║{CyberColors.NEON_CYAN}               • Parallel Processing{CyberColors.NEON_GREEN}                                         ║",
            f"║{CyberColors.NEON_CYAN}               • Real-Time Monitoring{CyberColors.NEON_GREEN}                                        ║",
            "║                                                                              ║",
            "╚══════════════════════════════════════════════════════════════════════════════╝",
            f"{CyberColors.RESET}"
        ]
        
        # Animate banner with typewriter effect
        for line in banner_lines:
            print(line)
            time.sleep(0.02)
        
        # Matrix rain effect
        print(f"\n{CyberColors.NEON_GREEN}Initializing Transfer Matrix...{CyberColors.RESET}")
        AnimationEngine.matrix_rain(15, 1.5)
        
        # Hacking effect
        AnimationEngine.hack_effect("⚡ SYSTEM INITIALIZED - READY FOR TRANSFER", CyberColors.NEON_GREEN)
        print(f"{CyberColors.NEON_BLUE}{'=' * 70}{CyberColors.RESET}\n")
    
    @staticmethod
    def display_shutdown_banner():
        """Display shutdown banner"""
        print(f"\n{CyberColors.NEON_RED}")
        print("╔══════════════════════════════════════════════════════════════════╗")
        print("║                                                                  ║")
        print("║   ███████╗██╗  ██╗██╗   ██╗████████╗██████╗  ██████╗ ██╗    ██╗ ║")
        print("║   ██╔════╝██║  ██║██║   ██║╚══██╔══╝██╔══██╗██╔═══██╗██║    ██║ ║")
        print("║   ███████╗███████║██║   ██║   ██║   ██████╔╝██║   ██║██║ █╗ ██║ ║")
        print("║   ╚════██║██╔══██║██║   ██║   ██║   ██╔══██╗██║   ██║██║███╗██║ ║")
        print("║   ███████║██║  ██║╚██████╔╝   ██║   ██║  ██║╚██████╔╝╚███╔███╔╝ ║")
        print("║   ╚══════╝╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝ ╚═════╝  ╚══╝╚══╝  ║")
        print("║                                                                  ║")
        print("║           SYSTEM SHUTDOWN COMPLETE                               ║")
        print("║           TRANSMISSION TERMINATED                                ║")
        print("╚══════════════════════════════════════════════════════════════════╝")
        print(f"{CyberColors.RESET}")

# ============================================================
#  CONSTANTS & CONFIGURATION
# ============================================================

__version__ = "2.0.0"

DEFAULT_PORT = 65432
BUFFER_SIZE = 16384
FORMAT = 'utf-8'
CHUNK_SIZE = 1024 * 1024
MAX_RETRIES = 5
TIMEOUT = 60
HEARTBEAT_INTERVAL = 5
MAX_CONNECTIONS = 50
MAX_PARALLEL_TRANSFERS = 8
SECURITY_LEVEL_DEFAULT = 3

# ============================================================
#  LOGGING SETUP
# ============================================================

class CyberLogger:
    """Cyber-themed logger with colored output"""
    
    @staticmethod
    def info(message: str):
        print(f"{CyberColors.NEON_BLUE}[INFO]{CyberColors.RESET} {message}")
    
    @staticmethod
    def success(message: str):
        print(f"{CyberColors.NEON_GREEN}[SUCCESS]{CyberColors.RESET} {message}")
    
    @staticmethod
    def warning(message: str):
        print(f"{CyberColors.NEON_ORANGE}[WARNING]{CyberColors.RESET} {message}")
    
    @staticmethod
    def error(message: str):
        print(f"{CyberColors.NEON_RED}[ERROR]{CyberColors.RESET} {message}")
    
    @staticmethod
    def debug(message: str):
        print(f"{CyberColors.DIM}[DEBUG]{CyberColors.RESET} {message}")
    
    @staticmethod
    def status(message: str, status_type: str = "INFO"):
        colors = {
            "INFO": CyberColors.NEON_BLUE,
            "SUCCESS": CyberColors.NEON_GREEN,
            "WARNING": CyberColors.NEON_ORANGE,
            "ERROR": CyberColors.NEON_RED,
            "SYSTEM": CyberColors.NEON_PURPLE
        }
        color = colors.get(status_type, CyberColors.WHITE)
        print(f"{color}[{status_type}]{CyberColors.RESET} {message}")

logger = CyberLogger()

# ============================================================
#  ADVANCED ENUMS & DATA CLASSES
# ============================================================

class TransferStatus(Enum):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    PAUSED = 'paused'
    COMPLETED = 'completed'
    FAILED = 'failed'
    CANCELLED = 'cancelled'
    RESUMING = 'resuming'
    VERIFYING = 'verifying'

class ProtocolState(Enum):
    DISCONNECTED = auto()
    HANDSHAKE_INIT = auto()
    HANDSHAKE_COMPLETE = auto()
    AUTHENTICATING = auto()
    TRANSFER_NEGOTIATION = auto()
    TRANSFER_ACTIVE = auto()
    TRANSFER_PAUSED = auto()
    TRANSFER_RESUMING = auto()
    TRANSFER_COMPLETE = auto()
    TRANSFER_FAILED = auto()
    DISCONNECTING = auto()

class TransferMode(Enum):
    STANDARD = auto()
    HIGH_SPEED = auto()
    SECURE = auto()
    RESILIENT = auto()
    ADAPTIVE = auto()
    BATCH = auto()
    MIRROR = auto()
    STREAM = auto()

class MessageType(Enum):
    HANDSHAKE = 'HANDSHAKE'
    FILE_INFO = 'FILE_INFO'
    FILE_CHUNK = 'FILE_CHUNK'
    DIRECTORY_INFO = 'DIRECTORY_INFO'
    ACK = 'ACK'
    NACK = 'NACK'
    COMPLETE = 'COMPLETE'
    RESUME = 'RESUME'
    CANCEL = 'CANCEL'
    PAUSE = 'PAUSE'
    RESUME_TRANSFER = 'RESUME_TRANSFER'
    METADATA = 'METADATA'
    CHECKSUM = 'CHECKSUM'
    ERROR = 'ERROR'
    HEARTBEAT = 'HEARTBEAT'
    STATUS_REQUEST = 'STATUS_REQUEST'
    STATUS_RESPONSE = 'STATUS_RESPONSE'
    BATCH_INFO = 'BATCH_INFO'
    AUTH = 'AUTH'
    AUTH_RESPONSE = 'AUTH_RESPONSE'

@dataclass
class EnhancedTransferMetadata:
    transfer_id: str = field(default_factory=lambda: f"ZHV-{int(time.time())}-{os.urandom(4).hex()}")
    filename: str = ""
    file_size: int = 0
    checksum: str = ""
    checksum_algorithm: str = "sha512"
    compression_algorithm: str = "zlib"
    encryption_algorithm: str = "AES-256-GCM"
    encryption_key_id: str = ""
    iv: bytes = field(default_factory=lambda: os.urandom(16))
    auth_tag: bytes = field(default_factory=lambda: os.urandom(16))
    destination: str = ""
    source_system: str = ""
    destination_system: str = ""
    source_user: str = ""
    destination_user: str = ""
    session_id: str = ""
    chunk_size: int = CHUNK_SIZE
    parallelism: int = 1
    compression_level: int = 6
    priority: int = 0
    resume_offset: int = 0
    total_chunks: int = 0
    completed_chunks: int = 0
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    
    def to_bytes(self) -> bytes:
        return pickle.dumps(self, protocol=pickle.HIGHEST_PROTOCOL)
    
    @classmethod
    def from_bytes(cls, data: bytes) -> 'EnhancedTransferMetadata':
        return pickle.loads(data)

@dataclass
class TransferProgress:
    transfer_id: str
    filename: str
    total_size: int
    bytes_transferred: int
    status: TransferStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    speed: float = 0.0
    eta: float = 0.0
    chunks_completed: int = 0
    total_chunks: int = 0
    
    @property
    def progress_percentage(self) -> float:
        if self.total_size == 0:
            return 0.0
        return (self.bytes_transferred / self.total_size) * 100
    
    @property
    def elapsed_time(self) -> float:
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return (datetime.now() - self.start_time).total_seconds()

# ============================================================
#  SECURE TRANSPORT LAYER
# ============================================================

class SecureTransportLayer:
    def __init__(self):
        self.ssl_context = None
        self.aes_key = None
        self.rsa_keypair = None
        self.session_key = None
        self.security_level = SECURITY_LEVEL_DEFAULT
        
    def initialize_security(self, security_level: int = SECURITY_LEVEL_DEFAULT):
        self.security_level = min(5, max(1, security_level))
        self.aes_key = os.urandom(32)
        
        if self.security_level >= 3:
            self._generate_rsa_keypair()
            self._setup_ssl_context()
    
    def _generate_rsa_keypair(self):
        try:
            from cryptography.hazmat.primitives.asymmetric import rsa
            from cryptography.hazmat.primitives import serialization
            key_size = 4096 if self.security_level >= 4 else 3072
            self.rsa_keypair = rsa.generate_private_key(
                public_exponent=65537,
                key_size=key_size
            )
        except ImportError:
            logger.warning("cryptography module not available for RSA")
    
    def _setup_ssl_context(self):
        try:
            self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            self.ssl_context.minimum_version = ssl.TLSVersion.TLSv1_3
            self.ssl_context.set_ciphers('ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM')
            self.ssl_context.options |= ssl.OP_NO_COMPRESSION
            self.ssl_context.check_hostname = False
        except AttributeError:
            self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    
    def encrypt_chunk(self, data: bytes) -> bytes:
        try:
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
            from cryptography.hazmat.primitives import hashes, padding
            
            if self.security_level >= 2:
                aesgcm = AESGCM(self.aes_key)
                nonce = os.urandom(12)
                encrypted = aesgcm.encrypt(nonce, data, b'')
                data = nonce + encrypted
                
            if self.security_level >= 4 and self.rsa_keypair:
                from cryptography.hazmat.primitives.asymmetric import padding
                signature = self.rsa_keypair.sign(
                    data,
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA512()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA512()
                )
                data = signature + data
                
            return data
        except ImportError:
            return base64.b64encode(data)
    
    def decrypt_chunk(self, data: bytes) -> bytes:
        try:
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
            from cryptography.hazmat.primitives import hashes, padding
            from cryptography.hazmat.primitives.asymmetric import padding
            
            if self.security_level >= 4 and self.rsa_keypair:
                signature_length = 512 if self.security_level >= 4 else 384
                signature, data = data[:signature_length], data[signature_length:]
                try:
                    self.rsa_keypair.public_key().verify(
                        signature,
                        data,
                        padding.PSS(
                            mgf=padding.MGF1(hashes.SHA512()),
                            salt_length=padding.PSS.MAX_LENGTH
                        ),
                        hashes.SHA512()
                    )
                except Exception:
                    raise ValueError("Signature verification failed")
                    
            if self.security_level >= 2:
                nonce = data[:12]
                encrypted = data[12:]
                aesgcm = AESGCM(self.aes_key)
                data = aesgcm.decrypt(nonce, encrypted, b'')
                
            return data
        except ImportError:
            return base64.b64decode(data)

# ============================================================
#  ADAPTIVE FLOW CONTROLLER
# ============================================================

class AdaptiveFlowController:
    def __init__(self, target_bandwidth_mbps: float = 100):
        self.target_bandwidth = target_bandwidth_mbps * 1024 * 1024 / 8
        self.current_bandwidth = self.target_bandwidth * 0.5
        self.min_bandwidth = 1024 * 1024 / 8
        self.max_bandwidth = self.target_bandwidth * 1.5
        self.cwnd = 1
        self.ssthresh = 64
        self.rtt_samples = collections.deque(maxlen=10)
        self.loss_rate = 0.0
        self.packet_loss_count = 0
        self.total_packets = 0
        self.stats = {
            'bytes_sent': 0,
            'bytes_received': 0,
            'packets_sent': 0,
            'packets_received': 0,
            'retransmissions': 0,
            'congestion_events': 0,
            'throughput_mbps': 0,
            'rtt_ms': 0,
            'available_bandwidth_mbps': 0
        }
        self.lock = threading.Lock()
        
    def update_rtt(self, rtt_ms: float):
        with self.lock:
            self.rtt_samples.append(rtt_ms)
            if self.rtt_samples:
                avg_rtt = sum(self.rtt_samples) / len(self.rtt_samples)
                self.stats['rtt_ms'] = avg_rtt
                if avg_rtt > 50:
                    self.current_bandwidth *= 0.95
                elif avg_rtt < 10:
                    self.current_bandwidth = min(
                        self.current_bandwidth * 1.05,
                        self.max_bandwidth
                    )
    
    def on_packet_loss(self):
        with self.lock:
            self.packet_loss_count += 1
            self.total_packets += 1
            self.loss_rate = self.packet_loss_count / max(1, self.total_packets)
            if self.cwnd > self.ssthresh:
                self.cwnd *= 0.5
            else:
                self.ssthresh = max(2, self.cwnd // 2)
                self.cwnd = 1
            self.stats['congestion_events'] += 1
            self.stats['retransmissions'] += 1
    
    def on_packet_success(self):
        with self.lock:
            self.total_packets += 1
            if self.cwnd < self.ssthresh:
                self.cwnd *= 2
            else:
                self.cwnd += 1 / self.cwnd
            self._update_throughput()
    
    def _update_throughput(self):
        throughput = self.current_bandwidth * (1 - self.loss_rate) * 0.9
        self.current_bandwidth = max(
            self.min_bandwidth,
            min(throughput, self.max_bandwidth)
        )
        self.stats['throughput_mbps'] = self.current_bandwidth / (1024 * 1024 / 8)
        self.stats['available_bandwidth_mbps'] = self.stats['throughput_mbps']
    
    def get_chunk_size(self) -> int:
        base_size = 64 * 1024
        rtt = self.stats.get('rtt_ms', 20)
        if rtt < 20:
            size_multiplier = 2.0
        elif rtt < 50:
            size_multiplier = 1.0
        else:
            size_multiplier = 0.5
        bandwidth_factor = self.current_bandwidth / (100 * 1024 * 1024 / 8)
        size_multiplier *= max(0.5, min(2.0, bandwidth_factor))
        loss_penalty = 1.0 - self.loss_rate * 5
        size_multiplier *= max(0.25, min(1.0, loss_penalty))
        chunk_size = int(base_size * size_multiplier)
        return max(8 * 1024, min(1024 * 1024, chunk_size))
    
    def get_current_bandwidth(self) -> float:
        return self.current_bandwidth
    
    def get_stats(self) -> Dict[str, Any]:
        with self.lock:
            return self.stats.copy()

# ============================================================
#  PERFORMANCE METRICS SYSTEM
# ============================================================

class PerformanceMetrics:
    def __init__(self):
        self.metrics = {
            'throughput': collections.deque(maxlen=100),
            'latency': collections.deque(maxlen=100),
            'cpu_usage': collections.deque(maxlen=100),
            'memory_usage': collections.deque(maxlen=100),
            'io_wait': collections.deque(maxlen=100),
            'network_bandwidth': collections.deque(maxlen=100),
            'packet_loss': collections.deque(maxlen=100),
            'retransmission_rate': collections.deque(maxlen=100),
            'concurrent_transfers': collections.deque(maxlen=100)
        }
        self.timestamps = collections.deque(maxlen=100)
        self.start_time = time.time()
        self._lock = threading.Lock()
        
    def record_metric(self, name: str, value: float):
        with self._lock:
            if name in self.metrics:
                self.metrics[name].append(value)
                self.timestamps.append(time.time())
    
    def get_report(self) -> Dict[str, Any]:
        with self._lock:
            report = {
                'timestamp': datetime.utcnow().isoformat(),
                'uptime_seconds': time.time() - self.start_time,
                'metrics': {}
            }
            for name, values in self.metrics.items():
                if values:
                    report['metrics'][name] = {
                        'current': values[-1],
                        'average': sum(values) / len(values),
                        'max': max(values),
                        'min': min(values),
                        'stddev': self._calculate_stddev(values)
                    }
            return report
    
    def _calculate_stddev(self, values: List[float]) -> float:
        if len(values) < 2:
            return 0.0
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
        return math.sqrt(variance)

# ============================================================
#  CORE PROTOCOL IMPLEMENTATION
# ============================================================

class ZhaevaProtocol:
    PROTOCOL_VERSION = "2.0"
    MAGIC_BYTES = b"ZHAEVA"
    
    @staticmethod
    def create_message(msg_type: MessageType, data: Any = None, 
                      compress: bool = False) -> bytes:
        message = {
            'magic': ZhaevaProtocol.MAGIC_BYTES.hex(),
            'version': ZhaevaProtocol.PROTOCOL_VERSION,
            'type': msg_type.value,
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        serialized = pickle.dumps(message, protocol=pickle.HIGHEST_PROTOCOL)
        if compress and len(serialized) > 1024:
            serialized = zlib.compress(serialized, level=6)
            message['compressed'] = True
        msg_length = len(serialized)
        return msg_length.to_bytes(8, byteorder='big') + serialized
    
    @staticmethod
    def parse_message(data: bytes) -> Dict[str, Any]:
        if len(data) < 8:
            raise ValueError("Message too short")
        msg_length = int.from_bytes(data[:8], byteorder='big')
        payload = data[8:8+msg_length]
        if len(payload) > 0 and payload[:2] == b'\x78\x9c':
            payload = zlib.decompress(payload)
        try:
            message = pickle.loads(payload)
        except pickle.UnpicklingError:
            raise ValueError("Invalid message format")
        if message.get('magic') != ZhaevaProtocol.MAGIC_BYTES.hex():
            raise ValueError("Invalid magic bytes")
        return message

# ============================================================
#  CORE TRANSFER ENGINE
# ============================================================

class ZhaevaEngine:
    def __init__(self, host='0.0.0.0', port=DEFAULT_PORT, 
                 use_ssl=False, cert_file=None, key_file=None,
                 security_level=SECURITY_LEVEL_DEFAULT):
        self.host = host
        self.port = port
        self.use_ssl = use_ssl
        self.cert_file = cert_file
        self.key_file = key_file
        self.security_level = security_level
        self.socket = None
        self.ssl_context = None
        self.is_paused = False
        self.is_cancelled = False
        self.transfer_queue = queue.PriorityQueue()
        self.active_transfers: Dict[str, TransferProgress] = {}
        self.completed_transfers: List[TransferProgress] = []
        self.failed_transfers: List[TransferProgress] = []
        self.transfer_history: List[Dict] = []
        self.engine_id = f"zhaeva-{int(time.time())}"
        self.heartbeat_thread = None
        self.running = False
        self._current_file = None
        self._current_path = None
        self._bytes_received = 0
        self._chunks_received = {}
        self._received_files: Dict[str, str] = {}
        self.transfer_mode = TransferMode.ADAPTIVE
        self.max_parallel_transfers = MAX_PARALLEL_TRANSFERS
        self.parallel_executor = None
        self._lock = threading.Lock()
        
        self.secure_transport = SecureTransportLayer()
        self.secure_transport.initialize_security(security_level)
        
        self.flow_controller = AdaptiveFlowController()
        self.metrics = PerformanceMetrics()
        self.state = ProtocolState.DISCONNECTED
        
        if use_ssl:
            self._setup_ssl()
    
    def _setup_ssl(self):
        if self.secure_transport.ssl_context:
            self.ssl_context = self.secure_transport.ssl_context
            return
        self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        if self.cert_file and self.key_file:
            try:
                self.ssl_context.load_cert_chain(
                    certfile=self.cert_file, 
                    keyfile=self.key_file
                )
                logger.success(f"SSL certificates loaded from {self.cert_file}")
            except Exception as e:
                logger.error(f"Failed to load SSL certificates: {e}")
                self.ssl_context = None
        else:
            self._generate_self_signed_cert()
    
    def _generate_self_signed_cert(self):
        try:
            from cryptography import x509
            from cryptography.x509.oid import NameOID
            from cryptography.hazmat.primitives import hashes, serialization
            from cryptography.hazmat.primitives.asymmetric import rsa
            import datetime as dt
            
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
            )
            subject = issuer = x509.Name([
                x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
                x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "State"),
                x509.NameAttribute(NameOID.LOCALITY_NAME, "City"),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Zhaeva Transfer"),
                x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
            ])
            cert = x509.CertificateBuilder().subject_name(
                subject
            ).issuer_name(
                issuer
            ).public_key(
                private_key.public_key()
            ).serial_number(
                x509.random_serial_number()
            ).not_valid_before(
                dt.datetime.utcnow()
            ).not_valid_after(
                dt.datetime.utcnow() + dt.timedelta(days=365)
            ).add_extension(
                x509.SubjectAlternativeName([
                    x509.DNSName("localhost"),
                    x509.DNSName("*.local"),
                ]),
                critical=False,
            ).sign(private_key, hashes.SHA256())
            
            with open("zhaeva_server.key", "wb") as f:
                f.write(private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                ))
            with open("zhaeva_server.crt", "wb") as f:
                f.write(cert.public_bytes(serialization.Encoding.PEM))
            
            logger.success("Generated self-signed SSL certificate")
            if self.ssl_context:
                try:
                    self.ssl_context.load_cert_chain(
                        certfile='zhaeva_server.crt', 
                        keyfile='zhaeva_server.key'
                    )
                except:
                    logger.warning("Could not load self-signed certificate")
        except ImportError:
            logger.warning("cryptography module not installed. SSL disabled.")
            self.ssl_context = None
    
    def _create_socket(self, is_server=False) -> socket.socket:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(TIMEOUT)
        if is_server and self.use_ssl and self.ssl_context:
            return self.ssl_context.wrap_socket(sock, server_side=True)
        elif not is_server and self.use_ssl and self.ssl_context:
            return self.ssl_context.wrap_socket(sock, server_side=False)
        return sock
    
    def calculate_checksum(self, filepath: str, algorithm: str = 'sha512') -> str:
        try:
            hash_func = hashlib.new(algorithm)
        except ValueError:
            hash_func = hashlib.sha256()
            algorithm = 'sha256'
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(BUFFER_SIZE), b''):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    
    def compress_data(self, data: bytes) -> bytes:
        return zlib.compress(data, level=6)
    
    def decompress_data(self, data: bytes) -> bytes:
        return zlib.decompress(data)
    
    def encrypt_chunk(self, data: bytes) -> bytes:
        return self.secure_transport.encrypt_chunk(data)
    
    def decrypt_chunk(self, data: bytes) -> bytes:
        return self.secure_transport.decrypt_chunk(data)
    
    def send_message(self, sock: socket.socket, msg_type: MessageType, 
                     data: Any = None, compress: bool = False) -> bool:
        try:
            message = ZhaevaProtocol.create_message(msg_type, data, compress)
            sock.send(message)
            return True
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            return False
    
    def receive_message(self, sock: socket.socket) -> Optional[Dict[str, Any]]:
        try:
            length_data = sock.recv(8)
            if not length_data:
                return None
            msg_length = int.from_bytes(length_data, byteorder='big')
            data = b''
            while len(data) < msg_length:
                chunk = sock.recv(min(BUFFER_SIZE, msg_length - len(data)))
                if not chunk:
                    break
                data += chunk
            if len(data) < msg_length:
                logger.warning(f"Incomplete message: {len(data)}/{msg_length}")
                return None
            return ZhaevaProtocol.parse_message(length_data + data)
        except socket.timeout:
            return None
        except Exception as e:
            logger.error(f"Failed to receive message: {e}")
            return None
    
    def send_heartbeat(self, sock: socket.socket):
        while self.running:
            try:
                time.sleep(HEARTBEAT_INTERVAL)
                if sock:
                    self.send_message(sock, MessageType.HEARTBEAT, 
                                    {'engine_id': self.engine_id})
            except Exception:
                break
    
    def transfer_file_parallel(self, sock: socket.socket, filepath: str, 
                               dest_path: str = None, compress: bool = False,
                               num_workers: int = 2) -> bool:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        filesize = os.path.getsize(filepath)
        filename = os.path.basename(filepath)
        chunk_size = self.flow_controller.get_chunk_size()
        total_chunks = (filesize + chunk_size - 1) // chunk_size
        
        metadata = EnhancedTransferMetadata(
            filename=filename,
            file_size=filesize,
            checksum=self.calculate_checksum(filepath),
            checksum_algorithm="sha512",
            chunk_size=chunk_size,
            total_chunks=total_chunks,
            parallelism=num_workers,
            destination=dest_path or filename
        )
        
        logger.status(f"⚡ Initiating parallel transfer: {filename} ({filesize:,} bytes, {num_workers} workers)", "SYSTEM")
        
        if not self.send_message(sock, MessageType.METADATA, asdict(metadata)):
            raise Exception("Failed to send metadata")
        
        response = self.receive_message(sock)
        if not response or response['type'] != MessageType.ACK.value:
            raise Exception("Server did not acknowledge metadata")
        
        progress = TransferProgress(
            transfer_id=metadata.transfer_id,
            filename=filename,
            total_size=filesize,
            bytes_transferred=0,
            status=TransferStatus.IN_PROGRESS,
            start_time=datetime.now(),
            total_chunks=total_chunks
        )
        self.active_transfers[metadata.transfer_id] = progress
        
        AnimationEngine.pulse_animation(f"🚀 Transferring {filename}", 1.0)
        
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            futures = []
            for chunk_num in range(total_chunks):
                future = executor.submit(
                    self._transfer_chunk,
                    sock, filepath, chunk_num, chunk_size,
                    filesize, compress, metadata
                )
                futures.append(future)
            
            success = True
            completed = 0
            with tqdm.tqdm(total=total_chunks, desc=f"{CyberColors.NEON_BLUE}Chunks{CyberColors.RESET}", 
                          bar_format=f"{{l_bar}}{CyberColors.NEON_GREEN}{{bar}}{CyberColors.RESET}{{r_bar}}") as pbar:
                for future in as_completed(futures):
                    try:
                        result = future.result()
                        if not result:
                            success = False
                        completed += 1
                        pbar.update(1)
                        with self._lock:
                            progress = self.active_transfers.get(metadata.transfer_id)
                            if progress:
                                progress.bytes_transferred = int((completed / total_chunks) * filesize)
                                progress.chunks_completed = completed
                    except Exception as e:
                        logger.error(f"Chunk transfer failed: {e}")
                        success = False
        
        if success:
            progress.status = TransferStatus.COMPLETED
            progress.end_time = datetime.now()
            self.completed_transfers.append(progress)
            self.transfer_history.append({
                'transfer_id': metadata.transfer_id,
                'filename': filename,
                'size': filesize,
                'status': 'completed',
                'timestamp': datetime.now().isoformat()
            })
            logger.success(f"✅ Parallel transfer completed: {filename}")
        else:
            progress.status = TransferStatus.FAILED
            progress.end_time = datetime.now()
            self.failed_transfers.append(progress)
            logger.error(f"❌ Parallel transfer failed: {filename}")
        
        if metadata.transfer_id in self.active_transfers:
            del self.active_transfers[metadata.transfer_id]
        
        return success
    
    def _transfer_chunk(self, sock: socket.socket, filepath: str,
                        chunk_num: int, chunk_size: int, filesize: int,
                        compress: bool, metadata: EnhancedTransferMetadata) -> bool:
        try:
            with open(filepath, 'rb') as f:
                offset = chunk_num * chunk_size
                f.seek(offset)
                chunk = f.read(chunk_size)
                if not chunk:
                    return True
                if compress:
                    chunk = self.compress_data(chunk)
                if self.security_level >= 2:
                    chunk = self.encrypt_chunk(chunk)
                chunk_data = {
                    'transfer_id': metadata.transfer_id,
                    'chunk_number': chunk_num,
                    'total_chunks': metadata.total_chunks,
                    'offset': offset,
                    'data': chunk,
                    'size': len(chunk),
                    'compressed': compress,
                    'encrypted': self.security_level >= 2
                }
                for attempt in range(MAX_RETRIES):
                    if self.send_message(sock, MessageType.FILE_CHUNK, chunk_data):
                        ack = self.receive_message(sock)
                        if ack and ack['type'] == MessageType.ACK.value:
                            return True
                    self.flow_controller.on_packet_loss()
                    time.sleep(0.1 * (attempt + 1))
                return False
        except Exception as e:
            logger.error(f"Chunk transfer error: {e}")
            return False
    
    def transfer_file(self, sock: socket.socket, filepath: str, 
                     dest_path: str = None, compress: bool = False) -> bool:
        transfer_id = f"transfer-{int(time.time())}"
        
        try:
            if not os.path.exists(filepath):
                raise FileNotFoundError(f"File not found: {filepath}")
            
            filesize = os.path.getsize(filepath)
            filename = os.path.basename(filepath)
            checksum = self.calculate_checksum(filepath)
            
            progress = TransferProgress(
                transfer_id=transfer_id,
                filename=filename,
                total_size=filesize,
                bytes_transferred=0,
                status=TransferStatus.IN_PROGRESS,
                start_time=datetime.now()
            )
            self.active_transfers[transfer_id] = progress
            
            metadata = EnhancedTransferMetadata(
                filename=filename,
                file_size=filesize,
                checksum=checksum,
                compression_algorithm="zlib" if compress else "none",
                encryption_algorithm="AES-256-GCM" if self.security_level >= 2 else "none",
                chunk_size=CHUNK_SIZE,
                destination=dest_path or filename
            )
            
            logger.status(f"📤 Sending file: {filename} ({filesize:,} bytes)", "SYSTEM")
            
            if not self.send_message(sock, MessageType.FILE_INFO, asdict(metadata)):
                raise Exception("Failed to send file metadata")
            
            response = self.receive_message(sock)
            if not response or response['type'] != MessageType.ACK.value:
                raise Exception("Server did not acknowledge file info")
            
            bar = tqdm.tqdm(total=filesize, desc=f"{CyberColors.NEON_BLUE}Uploading{CyberColors.RESET}",
                           unit='B', unit_scale=True, 
                           bar_format=f"{{l_bar}}{CyberColors.NEON_GREEN}{{bar}}{CyberColors.RESET}{{r_bar}}")
            
            with open(filepath, 'rb') as f:
                bytes_sent = 0
                chunk_number = 0
                
                while bytes_sent < filesize:
                    if self.is_cancelled:
                        self.send_message(sock, MessageType.CANCEL)
                        bar.close()
                        progress.status = TransferStatus.CANCELLED
                        logger.warning("Transfer cancelled by user")
                        return False
                    
                    while self.is_paused:
                        progress.status = TransferStatus.PAUSED
                        time.sleep(0.1)
                    
                    progress.status = TransferStatus.IN_PROGRESS
                    chunk = f.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    
                    if compress:
                        chunk = self.compress_data(chunk)
                    if self.security_level >= 2:
                        chunk = self.encrypt_chunk(chunk)
                    
                    chunk_data = {
                        'chunk_number': chunk_number,
                        'data': chunk,
                        'size': len(chunk),
                        'compressed': compress,
                        'encrypted': self.security_level >= 2
                    }
                    
                    if not self.send_message(sock, MessageType.FILE_CHUNK, 
                                           chunk_data, compress=False):
                        raise Exception(f"Failed to send chunk {chunk_number}")
                    
                    retries = 0
                    ack = None
                    while retries < MAX_RETRIES:
                        ack = self.receive_message(sock)
                        if ack and ack['type'] == MessageType.ACK.value:
                            break
                        retries += 1
                        self.flow_controller.on_packet_loss()
                        if retries % 3 == 0:
                            logger.warning(f"Retrying chunk {chunk_number} ({retries+1}/{MAX_RETRIES})")
                    
                    if not ack or ack['type'] != MessageType.ACK.value:
                        raise Exception(f"Failed to receive ACK for chunk {chunk_number}")
                    
                    self.flow_controller.on_packet_success()
                    bytes_sent += len(chunk)
                    chunk_number += 1
                    progress.bytes_transferred = bytes_sent
                    bar.update(len(chunk))
                    
                    elapsed = progress.elapsed_time
                    if elapsed > 0:
                        progress.speed = bytes_sent / elapsed
                        if progress.speed > 0:
                            progress.eta = (filesize - bytes_sent) / progress.speed
            
            bar.close()
            self.send_message(sock, MessageType.COMPLETE, {'checksum': checksum})
            
            final_response = self.receive_message(sock)
            if final_response and final_response['type'] == MessageType.COMPLETE.value:
                verified = final_response['data'].get('verified', False)
                if verified:
                    logger.success(f"✅ File {filename} transferred successfully!")
                    progress.status = TransferStatus.COMPLETED
                    progress.end_time = datetime.now()
                    self.completed_transfers.append(progress)
                    if transfer_id in self.active_transfers:
                        del self.active_transfers[transfer_id]
                    self.transfer_history.append({
                        'transfer_id': transfer_id,
                        'filename': filename,
                        'size': filesize,
                        'status': 'completed',
                        'timestamp': datetime.now().isoformat()
                    })
                    return True
                else:
                    logger.error(f"❌ File verification failed!")
                    progress.status = TransferStatus.FAILED
                    self.failed_transfers.append(progress)
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Transfer error: {e}")
            if transfer_id in self.active_transfers:
                progress = self.active_transfers[transfer_id]
                progress.status = TransferStatus.FAILED
                progress.end_time = datetime.now()
                self.failed_transfers.append(progress)
                if transfer_id in self.active_transfers:
                    del self.active_transfers[transfer_id]
            return False
    
    def transfer_directory(self, sock: socket.socket, dirpath: str, 
                          dest_path: str = None, compress: bool = False) -> bool:
        if not os.path.isdir(dirpath):
            raise NotADirectoryError(f"Not a directory: {dirpath}")
        
        files = []
        total_size = 0
        for root, _, filenames in os.walk(dirpath):
            for filename in filenames:
                full_path = os.path.join(root, filename)
                rel_path = os.path.relpath(full_path, dirpath)
                file_size = os.path.getsize(full_path)
                files.append({
                    'path': full_path,
                    'rel_path': rel_path,
                    'size': file_size,
                    'checksum': self.calculate_checksum(full_path)
                })
                total_size += file_size
        
        dir_info = {
            'dirname': os.path.basename(dirpath),
            'dest_path': dest_path or os.path.basename(dirpath),
            'file_count': len(files),
            'total_size': total_size,
            'files': files,
            'timestamp': datetime.now().isoformat()
        }
        
        logger.status(f"📁 Transferring directory: {dirpath} ({len(files)} files, {total_size:,} bytes)", "SYSTEM")
        
        if not self.send_message(sock, MessageType.DIRECTORY_INFO, dir_info):
            raise Exception("Failed to send directory info")
        
        response = self.receive_message(sock)
        if not response or response['type'] != MessageType.ACK.value:
            raise Exception("Server did not acknowledge directory info")
        
        successful = 0
        for file_info in files:
            dest = os.path.join(dest_path or '', file_info['rel_path']) if dest_path else file_info['rel_path']
            if self.transfer_file(sock, file_info['path'], dest, compress):
                successful += 1
            else:
                logger.error(f"Failed to transfer: {file_info['rel_path']}")
        
        if successful == len(files):
            logger.success(f"✅ Directory transferred successfully!")
            return True
        else:
            logger.warning(f"⚠️ Directory transfer partially completed: {successful}/{len(files)} files")
            return False
    
    def batch_transfer(self, sock: socket.socket, files: List[str], 
                      dest_dir: str = None, compress: bool = False) -> bool:
        valid_files = []
        for filepath in files:
            if os.path.exists(filepath):
                valid_files.append(filepath)
            else:
                logger.warning(f"File not found: {filepath}")
        
        if not valid_files:
            logger.error("No valid files to transfer")
            return False
        
        batch_info = {
            'total_files': len(valid_files),
            'files': [os.path.basename(f) for f in valid_files],
            'dest_dir': dest_dir or '.',
            'timestamp': datetime.now().isoformat()
        }
        
        logger.status(f"📦 Batch transfer: {len(valid_files)} files", "SYSTEM")
        
        if not self.send_message(sock, MessageType.BATCH_INFO, batch_info):
            raise Exception("Failed to send batch info")
        
        response = self.receive_message(sock)
        if not response or response['type'] != MessageType.ACK.value:
            raise Exception("Server did not acknowledge batch info")
        
        successful = 0
        for filepath in valid_files:
            dest = os.path.join(dest_dir or '', os.path.basename(filepath)) if dest_dir else None
            if self.transfer_file(sock, filepath, dest, compress):
                successful += 1
        
        return successful == len(valid_files)
    
    def get_status(self) -> Dict[str, Any]:
        return {
            'engine_id': self.engine_id,
            'state': self.state.value,
            'active_transfers': len(self.active_transfers),
            'completed_transfers': len(self.completed_transfers),
            'failed_transfers': len(self.failed_transfers),
            'active_list': [
                {
                    'filename': p.filename,
                    'progress': p.progress_percentage,
                    'speed': p.speed,
                    'eta': p.eta,
                    'chunks': f"{p.chunks_completed}/{p.total_chunks}"
                }
                for p in self.active_transfers.values()
            ],
            'history': self.transfer_history[-10:],
            'performance': self.metrics.get_report(),
            'network': self.flow_controller.get_stats(),
            'security_level': self.security_level
        }

# ============================================================
#  ZHAEVA SERVER
# ============================================================

class ZhaevaServer:
    def __init__(self, host='0.0.0.0', port=DEFAULT_PORT, 
                 save_dir='received_files', **kwargs):
        self.host = host
        self.port = port
        self.save_dir = save_dir
        self.engine = ZhaevaEngine(host, port, **kwargs)
        self.running = False
        self.clients = []
        self.client_threads = []
        self.server_socket = None
        self.connections = {}
        self._start_time = datetime.now()
        self._lock = threading.Lock()
        
        os.makedirs(save_dir, exist_ok=True)
        signal.signal(signal.SIGINT, self._shutdown)
        signal.signal(signal.SIGTERM, self._shutdown)
    
    def start(self):
        self.running = True
        
        try:
            self.server_socket = self.engine._create_socket(is_server=True)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(MAX_CONNECTIONS)
            
            self._display_server_banner()
            
            status_thread = threading.Thread(target=self._report_status, daemon=True)
            status_thread.start()
            
            while self.running:
                try:
                    client_socket, addr = self.server_socket.accept()
                    logger.info(f"📥 Client connected from {addr[0]}:{addr[1]}")
                    
                    client_thread = threading.Thread(
                        target=self._handle_client, 
                        args=(client_socket, addr)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                    with self._lock:
                        self.clients.append(client_socket)
                        self.client_threads.append(client_thread)
                        self.connections[addr] = {
                            'socket': client_socket,
                            'thread': client_thread,
                            'connected_at': datetime.now()
                        }
                    
                except socket.timeout:
                    continue
                except Exception as e:
                    if self.running:
                        logger.error(f"Server error: {e}")
                        
        except Exception as e:
            logger.error(f"Failed to start server: {e}")
        finally:
            self._cleanup()
    
    def _display_server_banner(self):
        print(f"\n{CyberColors.NEON_BLUE}")
        print("═" * 70)
        print(f"{CyberColors.NEON_GREEN}🚀 ZHAEVA FILE TRANSFER SERVER v2.0")
        print("═" * 70)
        print(f"{CyberColors.NEON_CYAN}📡 Listening on: {CyberColors.BRIGHT_WHITE}{self.host}:{self.port}")
        print(f"{CyberColors.NEON_CYAN}📁 Save directory: {CyberColors.BRIGHT_WHITE}{self.save_dir}")
        print(f"{CyberColors.NEON_CYAN}🔐 SSL Enabled: {CyberColors.BRIGHT_WHITE}{self.engine.use_ssl}")
        print(f"{CyberColors.NEON_CYAN}🛡️ Security Level: {CyberColors.BRIGHT_WHITE}{self.engine.security_level}")
        print(f"{CyberColors.NEON_CYAN}⚡ Transfer Mode: {CyberColors.BRIGHT_WHITE}{self.engine.transfer_mode.value}")
        print("═" * 70)
        print(f"{CyberColors.NEON_ORANGE}Press Ctrl+C to shutdown")
        print("═" * 70)
        print(f"{CyberColors.RESET}")
        
        AnimationEngine.pulse_animation("🔄 Server is ready for connections", 1.5)
    
    def _handle_client(self, client_socket: socket.socket, addr: tuple):
        transfer_id = None
        
        try:
            self.engine.send_message(client_socket, MessageType.HANDSHAKE, {
                'server': 'Zhaeva',
                'version': __version__,
                'features': ['ssl', 'compression', 'encryption', 'parallel', 'resume'],
                'security_level': self.engine.security_level,
                'engine_id': self.engine.engine_id
            })
            
            while self.running:
                message = self.engine.receive_message(client_socket)
                if not message:
                    break
                
                msg_type = message['type']
                data = message['data']
                
                if msg_type == MessageType.FILE_INFO.value:
                    transfer_id = self._handle_file_info(client_socket, data)
                elif msg_type == MessageType.METADATA.value:
                    transfer_id = self._handle_metadata(client_socket, data)
                elif msg_type == MessageType.DIRECTORY_INFO.value:
                    transfer_id = self._handle_directory_info(client_socket, data)
                elif msg_type == MessageType.FILE_CHUNK.value:
                    self._handle_file_chunk(client_socket, data, transfer_id)
                elif msg_type == MessageType.BATCH_INFO.value:
                    self._handle_batch_info(client_socket, data)
                elif msg_type == MessageType.CANCEL.value:
                    logger.warning(f"⏹️ Transfer cancelled by client")
                    break
                elif msg_type == MessageType.PAUSE.value:
                    logger.info(f"⏸️ Transfer paused by client")
                    self.engine.is_paused = True
                elif msg_type == MessageType.RESUME_TRANSFER.value:
                    logger.info(f"▶️ Transfer resumed by client")
                    self.engine.is_paused = False
                elif msg_type == MessageType.HEARTBEAT.value:
                    self.engine.send_message(client_socket, MessageType.HEARTBEAT, 
                                           {'status': 'alive', 'timestamp': datetime.now().isoformat()})
                elif msg_type == MessageType.STATUS_REQUEST.value:
                    status = self.engine.get_status()
                    self.engine.send_message(client_socket, MessageType.STATUS_RESPONSE, status)
                elif msg_type == MessageType.COMPLETE.value:
                    self._handle_completion(client_socket, data, transfer_id)
                else:
                    logger.warning(f"Unknown message type: {msg_type}")
                    
        except Exception as e:
            logger.error(f"Client handler error: {e}")
        finally:
            try:
                client_socket.close()
            except:
                pass
            with self._lock:
                if addr in self.connections:
                    del self.connections[addr]
                if client_socket in self.clients:
                    self.clients.remove(client_socket)
    
    def _handle_file_info(self, client_socket: socket.socket, data: dict) -> str:
        if 'filename' in data and 'file_size' in data:
            filename = data['filename']
            filesize = data['file_size']
            checksum = data.get('checksum', '')
            dest_path = data.get('destination', filename)
            compress = data.get('compressed', False)
        else:
            metadata = EnhancedTransferMetadata(**data)
            filename = metadata.filename
            filesize = metadata.file_size
            checksum = metadata.checksum
            dest_path = metadata.destination or filename
            compress = metadata.compression_algorithm != "none"
        
        save_path = os.path.join(self.save_dir, dest_path)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        if os.path.exists(save_path):
            base, ext = os.path.splitext(save_path)
            counter = 1
            while os.path.exists(f"{base}_{counter}{ext}"):
                counter += 1
            save_path = f"{base}_{counter}{ext}"
        
        transfer_id = f"recv-{int(time.time())}"
        
        progress = TransferProgress(
            transfer_id=transfer_id,
            filename=filename,
            total_size=filesize,
            bytes_transferred=0,
            status=TransferStatus.IN_PROGRESS,
            start_time=datetime.now()
        )
        self.engine.active_transfers[transfer_id] = progress
        
        self.engine.send_message(client_socket, MessageType.ACK, {
            'transfer_id': transfer_id,
            'save_path': save_path,
            'chunk_size': CHUNK_SIZE
        })
        
        self.engine._current_file = open(save_path, 'wb')
        self.engine._current_path = save_path
        self.engine._bytes_received = 0
        
        logger.info(f"📥 Receiving {filename} ({filesize:,} bytes) -> {save_path}")
        
        return transfer_id
    
    def _handle_metadata(self, client_socket: socket.socket, data: dict) -> str:
        metadata = EnhancedTransferMetadata(**data)
        filename = metadata.filename
        filesize = metadata.file_size
        dest_path = metadata.destination or filename
        
        save_path = os.path.join(self.save_dir, dest_path)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        if os.path.exists(save_path):
            base, ext = os.path.splitext(save_path)
            counter = 1
            while os.path.exists(f"{base}_{counter}{ext}"):
                counter += 1
            save_path = f"{base}_{counter}{ext}"
        
        transfer_id = metadata.transfer_id
        
        progress = TransferProgress(
            transfer_id=transfer_id,
            filename=filename,
            total_size=filesize,
            bytes_transferred=0,
            status=TransferStatus.IN_PROGRESS,
            start_time=datetime.now(),
            total_chunks=metadata.total_chunks
        )
        self.engine.active_transfers[transfer_id] = progress
        
        self.engine.send_message(client_socket, MessageType.ACK, {
            'transfer_id': transfer_id,
            'save_path': save_path,
            'chunk_size': metadata.chunk_size
        })
        
        self.engine._current_file = open(save_path, 'wb')
        self.engine._current_path = save_path
        self.engine._bytes_received = 0
        self.engine._chunks_received = {}
        
        logger.info(f"📥 Receiving {filename} ({filesize:,} bytes, {metadata.total_chunks} chunks) -> {save_path}")
        
        return transfer_id
    
    def _handle_file_chunk(self, client_socket: socket.socket, chunk_data: dict, 
                          transfer_id: str = None):
        chunk_number = chunk_data['chunk_number']
        chunk = chunk_data['data']
        compressed = chunk_data.get('compressed', False)
        encrypted = chunk_data.get('encrypted', False)
        offset = chunk_data.get('offset', 0)
        
        if encrypted and self.engine.security_level >= 2:
            try:
                chunk = self.engine.decrypt_chunk(chunk)
            except Exception as e:
                logger.error(f"Decryption failed for chunk {chunk_number}: {e}")
                self.engine.send_message(client_socket, MessageType.NACK, {'error': 'Decryption failed'})
                return
        
        if compressed:
            try:
                chunk = self.engine.decompress_data(chunk)
            except Exception as e:
                logger.error(f"Decompression failed for chunk {chunk_number}: {e}")
                self.engine.send_message(client_socket, MessageType.NACK, {'error': 'Decompression failed'})
                return
        
        if self.engine._current_file:
            self.engine._current_file.seek(offset)
            self.engine._current_file.write(chunk)
            self.engine._bytes_received += len(chunk)
            
            if transfer_id and transfer_id in self.engine.active_transfers:
                progress = self.engine.active_transfers[transfer_id]
                progress.bytes_transferred = self.engine._bytes_received
                progress.chunks_completed += 1
                self.engine.metrics.record_metric('throughput', len(chunk))
        
        self.engine.send_message(client_socket, MessageType.ACK, {
            'chunk': chunk_number,
            'received': self.engine._bytes_received
        })
    
    def _handle_directory_info(self, client_socket: socket.socket, data: dict) -> str:
        dirname = data['dirname']
        dest_path = data.get('dest_path', dirname)
        file_count = data['file_count']
        total_size = data.get('total_size', 0)
        
        save_path = os.path.join(self.save_dir, dest_path)
        os.makedirs(save_path, exist_ok=True)
        
        transfer_id = f"dir-{int(time.time())}"
        
        logger.info(f"📁 Receiving directory: {dirname} -> {save_path}")
        logger.info(f"   {file_count} files, {total_size:,} bytes")
        
        self.engine.send_message(client_socket, MessageType.ACK, {
            'transfer_id': transfer_id,
            'save_path': save_path
        })
        
        return transfer_id
    
    def _handle_batch_info(self, client_socket: socket.socket, data: dict):
        total_files = data['total_files']
        files = data['files']
        dest_dir = data.get('dest_dir', '.')
        
        logger.info(f"📦 Receiving batch: {total_files} files")
        for f in files:
            logger.info(f"   - {f}")
        
        self.engine.send_message(client_socket, MessageType.ACK)
    
    def _handle_completion(self, client_socket: socket.socket, data: dict, 
                          transfer_id: str):
        checksum = data.get('checksum')
        
        verified = False
        if self.engine._current_path and checksum:
            actual_checksum = self.engine.calculate_checksum(self.engine._current_path)
            verified = (actual_checksum == checksum)
            
            if verified:
                logger.success(f"✅ File verified: {checksum}")
            else:
                logger.error(f"❌ Checksum mismatch!")
                logger.error(f"   Expected: {checksum}")
                logger.error(f"   Actual:   {actual_checksum}")
        
        if self.engine._current_file:
            self.engine._current_file.close()
            self.engine._current_file = None
        
        if transfer_id and transfer_id in self.engine.active_transfers:
            progress = self.engine.active_transfers[transfer_id]
            progress.status = TransferStatus.COMPLETED if verified else TransferStatus.FAILED
            progress.end_time = datetime.now()
            
            if verified:
                self.engine.completed_transfers.append(progress)
                self.engine.transfer_history.append({
                    'transfer_id': transfer_id,
                    'filename': progress.filename,
                    'size': progress.total_size,
                    'status': 'completed',
                    'timestamp': datetime.now().isoformat()
                })
            else:
                self.engine.failed_transfers.append(progress)
            
            if transfer_id in self.engine.active_transfers:
                del self.engine.active_transfers[transfer_id]
        
        self.engine.send_message(client_socket, MessageType.COMPLETE, {
            'verified': verified,
            'transfer_id': transfer_id
        })
        
        if verified:
            logger.success(f"✅ Transfer completed successfully!")
        else:
            logger.warning(f"⚠️ Transfer completed with errors")
    
    def _report_status(self):
        while self.running:
            time.sleep(30)
            if self.running:
                status = {
                    'connections': len(self.clients),
                    'active_transfers': len(self.engine.active_transfers),
                    'completed': len(self.engine.completed_transfers),
                    'failed': len(self.engine.failed_transfers),
                    'uptime': str(datetime.now() - self._start_time)
                }
                logger.status(f"📊 Status: {status}", "SYSTEM")
    
    def _cleanup(self):
        logger.info("🧹 Cleaning up...")
        with self._lock:
            for client in self.clients:
                try:
                    client.close()
                except:
                    pass
            self.clients.clear()
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        if self.engine._current_file:
            try:
                self.engine._current_file.close()
            except:
                pass
        logger.success("✅ Server shutdown complete")
    
    def _shutdown(self, signum=None, frame=None):
        logger.warning("\n⚠️ Shutting down server...")
        self.running = False
        time.sleep(2)
        sys.exit(0)

# ============================================================
#  ZHAEVA CLIENT
# ============================================================

class ZhaevaClient:
    def __init__(self, host='localhost', port=DEFAULT_PORT, **kwargs):
        self.host = host
        self.port = port
        self.engine = ZhaevaEngine(host, port, **kwargs)
        self.socket = None
        self.connected = False
        self.server_info = None
        self.interactive = False
        self._lock = threading.Lock()
    
    def connect(self) -> bool:
        try:
            self.socket = self.engine._create_socket(is_server=False)
            self.socket.connect((self.host, self.port))
            self.connected = True
            self.engine.running = True
            self.engine.state = ProtocolState.HANDSHAKE_INIT
            
            handshake = self.engine.receive_message(self.socket)
            if handshake and handshake['type'] == MessageType.HANDSHAKE.value:
                self.server_info = handshake['data']
                logger.success(f"✅ Connected to Zhaeva Server v{self.server_info.get('version', 'unknown')}")
                logger.info(f"   Features: {', '.join(self.server_info.get('features', []))}")
                self.engine.state = ProtocolState.HANDSHAKE_COMPLETE
            else:
                raise Exception("Invalid handshake response")
            
            heartbeat_thread = threading.Thread(
                target=self.engine.send_heartbeat, 
                args=(self.socket,),
                daemon=True
            )
            heartbeat_thread.start()
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Connection failed: {e}")
            self.connected = False
            self.engine.state = ProtocolState.DISCONNECTED
            return False
    
    def disconnect(self):
        if hasattr(self, 'socket') and self.socket:
            try:
                self.socket.close()
            except:
                pass
        self.connected = False
        self.engine.running = False
        self.engine.state = ProtocolState.DISCONNECTING
    
    def send_file(self, filepath: str, dest_path: str = None, 
                  compress: bool = False, parallel: bool = False) -> bool:
        if not self.connected:
            if not self.connect():
                return False
        
        try:
            if parallel:
                return self.engine.transfer_file_parallel(
                    self.socket, filepath, dest_path, compress,
                    min(4, MAX_PARALLEL_TRANSFERS)
                )
            else:
                return self.engine.transfer_file(
                    self.socket, filepath, dest_path, compress
                )
        except Exception as e:
            logger.error(f"Send error: {e}")
            return False
    
    def send_directory(self, dirpath: str, dest_path: str = None, 
                      compress: bool = False) -> bool:
        if not self.connected:
            if not self.connect():
                return False
        
        try:
            return self.engine.transfer_directory(self.socket, dirpath, dest_path, compress)
        except Exception as e:
            logger.error(f"Directory send error: {e}")
            return False
    
    def send_batch(self, files: List[str], dest_dir: str = None,
                   compress: bool = False) -> bool:
        if not self.connected:
            if not self.connect():
                return False
        
        try:
            return self.engine.batch_transfer(self.socket, files, dest_dir, compress)
        except Exception as e:
            logger.error(f"Batch send error: {e}")
            return False
    
    def get_server_status(self) -> Optional[Dict]:
        if not self.connected:
            return None
        
        try:
            self.engine.send_message(self.socket, MessageType.STATUS_REQUEST)
            response = self.engine.receive_message(self.socket)
            if response and response['type'] == MessageType.STATUS_RESPONSE.value:
                return response['data']
        except Exception as e:
            logger.error(f"Status request failed: {e}")
            return None
        
        return None
    
    def pause(self):
        with self._lock:
            self.engine.is_paused = True
            if self.connected:
                self.engine.send_message(self.socket, MessageType.PAUSE)
        logger.info("⏸️ Transfer paused")
    
    def resume(self):
        with self._lock:
            self.engine.is_paused = False
            if self.connected:
                self.engine.send_message(self.socket, MessageType.RESUME_TRANSFER)
        logger.info("▶️ Transfer resumed")
    
    def cancel(self):
        with self._lock:
            self.engine.is_cancelled = True
            if self.connected:
                self.engine.send_message(self.socket, MessageType.CANCEL)
        logger.info("⏹️ Transfer cancelled")
    
    def interactive_mode(self):
        self.interactive = True
        
        CyberBanner.display_startup_banner()
        
        print("\n" + "=" * 70)
        print(f"{CyberColors.NEON_GREEN}📁 ZHAEVA FILE TRANSFER TOOL - CLIENT MODE")
        print("=" * 70)
        print(f"{CyberColors.NEON_CYAN}🖥️  Connected to: {CyberColors.BRIGHT_WHITE}{self.host}:{self.port}")
        print(f"{CyberColors.NEON_CYAN}🔐 SSL: {CyberColors.BRIGHT_WHITE}{'Enabled' if self.engine.use_ssl else 'Disabled'}")
        print(f"{CyberColors.NEON_CYAN}🛡️ Security Level: {CyberColors.BRIGHT_WHITE}{self.engine.security_level}")
        print("=" * 70)
        
        commands = [
            (f"{CyberColors.NEON_GREEN}send-file{CyberColors.RESET}", " <path> [dest]     - Send a single file"),
            (f"{CyberColors.NEON_GREEN}send-file-p{CyberColors.RESET}", "<path> [dest]   - Send file with parallel chunks"),
            (f"{CyberColors.NEON_GREEN}send-dir{CyberColors.RESET}", "  <path> [dest]      - Send a directory"),
            (f"{CyberColors.NEON_GREEN}send-batch{CyberColors.RESET}", "<path1> [path2]  - Send multiple files"),
            (f"{CyberColors.NEON_BLUE}status{CyberColors.RESET}", "                     - Show transfer status"),
            (f"{CyberColors.NEON_BLUE}history{CyberColors.RESET}", "                    - Show transfer history"),
            (f"{CyberColors.NEON_ORANGE}pause{CyberColors.RESET}", "                     - Pause current transfer"),
            (f"{CyberColors.NEON_ORANGE}resume{CyberColors.RESET}", "                    - Resume current transfer"),
            (f"{CyberColors.NEON_RED}cancel{CyberColors.RESET}", "                    - Cancel current transfer"),
            (f"{CyberColors.NEON_PURPLE}server-status{CyberColors.RESET}", "             - Get server status"),
            (f"{CyberColors.NEON_PURPLE}performance{CyberColors.RESET}", "              - Show performance metrics"),
            (f"{CyberColors.NEON_BLUE}help{CyberColors.RESET}", "                      - Show this help"),
            (f"{CyberColors.NEON_RED}quit{CyberColors.RESET}", "                      - Exit")
        ]
        
        for cmd, desc in commands:
            print(f"  {cmd} {desc}")
        print("=" * 70)
        
        while True:
            try:
                cmd = input(f"\n{CyberColors.NEON_GREEN}💻 > {CyberColors.RESET}").strip()
                if not cmd:
                    continue
                
                parts = cmd.split()
                command = parts[0].lower()
                
                if command in ('quit', 'exit', 'q'):
                    break
                elif command == 'help':
                    print("Available commands: send-file, send-file-p, send-dir, send-batch, status, history, pause, resume, cancel, server-status, performance, help, quit")
                elif command == 'send-file':
                    if len(parts) >= 2:
                        dest = parts[2] if len(parts) > 2 else None
                        self.send_file(parts[1], dest, False, False)
                    else:
                        print("Usage: send-file <path> [dest]")
                elif command == 'send-file-p':
                    if len(parts) >= 2:
                        dest = parts[2] if len(parts) > 2 else None
                        self.send_file(parts[1], dest, False, True)
                    else:
                        print("Usage: send-file-p <path> [dest]")
                elif command == 'send-dir':
                    if len(parts) >= 2:
                        dest = parts[2] if len(parts) > 2 else None
                        self.send_directory(parts[1], dest)
                    else:
                        print("Usage: send-dir <path> [dest]")
                elif command == 'send-batch':
                    if len(parts) >= 2:
                        self.send_batch(parts[1:])
                    else:
                        print("Usage: send-batch <path1> [path2] ...")
                elif command == 'pause':
                    self.pause()
                elif command == 'resume':
                    self.resume()
                elif command == 'cancel':
                    self.cancel()
                elif command == 'status':
                    self.show_status()
                elif command == 'history':
                    self.show_history()
                elif command == 'performance':
                    self.show_performance()
                elif command == 'server-status':
                    status = self.get_server_status()
                    if status:
                        print(f"\n{CyberColors.NEON_BLUE}📊 Server Status:{CyberColors.RESET}")
                        print(f"  Engine ID: {status.get('engine_id', 'N/A')}")
                        print(f"  State: {status.get('state', 'N/A')}")
                        print(f"  Active Transfers: {status.get('active_transfers', 0)}")
                        print(f"  Completed: {status.get('completed_transfers', 0)}")
                        print(f"  Failed: {status.get('failed_transfers', 0)}")
                        print(f"  Security Level: {status.get('security_level', 0)}")
                        if status.get('active_list'):
                            print("  Currently Active:")
                            for t in status['active_list']:
                                bar = AnimationEngine.progress_bar(t['progress'])
                                print(f"    - {t['filename']}: {bar} ({t['speed']/1024:.1f} KB/s)")
                    else:
                        print("❌ Failed to get server status")
                else:
                    print(f"Unknown command: {command}")
                    
            except KeyboardInterrupt:
                print(f"\n{CyberColors.NEON_RED}Exiting...{CyberColors.RESET}")
                break
            except Exception as e:
                print(f"Error: {e}")
        
        self.disconnect()
        CyberBanner.display_shutdown_banner()
    
    def show_status(self):
        if self.engine.active_transfers:
            print(f"\n{CyberColors.NEON_BLUE}📊 Active Transfers:{CyberColors.RESET}")
            for tid, progress in self.engine.active_transfers.items():
                pct = progress.progress_percentage
                speed = progress.speed / 1024 if progress.speed > 0 else 0
                eta = progress.eta if progress.eta > 0 else 0
                chunks = f"{progress.chunks_completed}/{progress.total_chunks}" if progress.total_chunks > 0 else "N/A"
                bar = AnimationEngine.progress_bar(pct)
                print(f"  {progress.filename}: {bar} ({speed:.1f} KB/s, ETA: {eta:.1f}s, Chunks: {chunks})")
        else:
            print("No active transfers")
    
    def show_history(self):
        if self.engine.transfer_history:
            print(f"\n{CyberColors.NEON_PURPLE}📜 Transfer History:{CyberColors.RESET}")
            for item in self.engine.transfer_history[-10:]:
                status_icon = "✅" if item['status'] == 'completed' else "❌"
                size = item['size'] / (1024 * 1024)
                print(f"  {status_icon} {item['filename']} ({size:.2f} MB) - {item['status']}")
        else:
            print("No transfer history")
    
    def show_performance(self):
        metrics = self.engine.metrics.get_report()
        print(f"\n{CyberColors.NEON_CYAN}📈 Performance Metrics:{CyberColors.RESET}")
        print(f"  Uptime: {metrics['uptime_seconds']:.0f}s")
        for name, stats in metrics['metrics'].items():
            if stats:
                print(f"  {name}: {stats['current']:.2f} (avg: {stats['average']:.2f})")

# ============================================================
#  COMMAND LINE INTERFACE
# ============================================================

class ZhaevaCLI:
    def __init__(self):
        self.server = None
        self.client = None
        self.args = None
    
    def parse_args(self):
        parser = argparse.ArgumentParser(
            description='Zhaeva - Advanced File Transfer System',
            epilog='Example: zhaeva --mode server --ssl --security-level 4'
        )
        
        parser.add_argument('--mode', choices=['server', 'client'], required=True,
                          help='Run as server or client')
        parser.add_argument('--host', default='localhost',
                          help='Host to bind/connect to')
        parser.add_argument('--port', type=int, default=DEFAULT_PORT,
                          help='Port to use (default: 65432)')
        parser.add_argument('--ssl', action='store_true',
                          help='Enable SSL encryption')
        parser.add_argument('--cert', help='SSL certificate file')
        parser.add_argument('--key', help='SSL key file')
        parser.add_argument('--security-level', type=int, default=SECURITY_LEVEL_DEFAULT,
                          choices=range(1, 6),
                          help='Security level 1-5 (default: 3)')
        parser.add_argument('--save-dir', default='received_files',
                          help='Directory to save received files (server)')
        parser.add_argument('--file', help='File to send (client)')
        parser.add_argument('--dir', help='Directory to send (client)')
        parser.add_argument('--batch', nargs='+', help='Multiple files to send')
        parser.add_argument('--dest', help='Destination path for file/directory')
        parser.add_argument('--compress', action='store_true',
                          help='Compress data during transfer')
        parser.add_argument('--parallel', action='store_true',
                          help='Use parallel chunk transfer')
        parser.add_argument('--verbose', action='store_true',
                          help='Enable verbose logging')
        parser.add_argument('--version', action='version',
                          version=f'Zhaeva v{__version__}')
        
        self.args = parser.parse_args()
        return self.args
    
    def run_server(self):
        self.server = ZhaevaServer(
            host=self.args.host,
            port=self.args.port,
            save_dir=self.args.save_dir,
            use_ssl=self.args.ssl,
            cert_file=self.args.cert,
            key_file=self.args.key,
            security_level=self.args.security_level
        )
        self.server.start()
    
    def run_client(self):
        self.client = ZhaevaClient(
            host=self.args.host,
            port=self.args.port,
            use_ssl=self.args.ssl,
            cert_file=self.args.cert,
            key_file=self.args.key,
            security_level=self.args.security_level
        )
        
        if not self.client.connect():
            return
        
        try:
            if self.args.file:
                self.client.send_file(self.args.file, self.args.dest, 
                                     self.args.compress, self.args.parallel)
            elif self.args.dir:
                self.client.send_directory(self.args.dir, self.args.dest, self.args.compress)
            elif self.args.batch:
                self.client.send_batch(self.args.batch, self.args.dest, self.args.compress)
            else:
                self.client.interactive_mode()
        finally:
            self.client.disconnect()
    
    def run(self):
        self.parse_args()
        
        if self.args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        
        if not self.args.file and not self.args.dir and not self.args.batch:
            CyberBanner.display_startup_banner()
        
        if self.args.mode == 'server':
            self.run_server()
        else:
            self.run_client()

# ============================================================
#  MAIN ENTRY POINT
# ============================================================

def main():
    cli = ZhaevaCLI()
    try:
        cli.run()
    except KeyboardInterrupt:
        print(f"\n\n{CyberColors.NEON_RED}👋 Zhaeva shutdown complete{CyberColors.RESET}")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
