import pytest
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.exceptions import InvalidSignature
from src.shared.security import create_signed_envelope, verify_and_extract_envelope

def test_envelope_creation_and_verification():
    # Generate throwaway keys for testing
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    
    # Create a fake event
    event_data = {"id": 101, "categoria": "livro", "preco": 45.00}
    
    # Create the envelope
    envelope = create_signed_envelope(event_data, private_key)
    
    assert "data" in envelope
    assert "signature" in envelope
    
    # Verify and extract
    extracted_data = verify_and_extract_envelope(envelope, public_key)
    assert extracted_data == event_data

def test_invalid_signature_is_rejected():
    private_key1 = ed25519.Ed25519PrivateKey.generate()
    private_key2 = ed25519.Ed25519PrivateKey.generate()
    public_key2 = private_key2.public_key() # Wrong public key!
    
    event_data = {"id": 102}
    
    # Sign with key 1
    envelope = create_signed_envelope(event_data, private_key1)
    
    # Try to verify with key 2
    with pytest.raises(InvalidSignature):
        verify_and_extract_envelope(envelope, public_key2)