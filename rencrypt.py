import click
from cryptography.fernet import Fernet


@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)


@cli.command(name="generate")
@click.pass_context
@click.option("--name", "-n", default="keyfile", prompt="Name of key file", help="The name of the output key file.")
def generate_key(ctx, name):
    """Generate a key file"""
    click.echo(f"Generating key file {name}.key...")

    # key generation
    key = Fernet.generate_key()

    # string the key in a file
    with open(f'{name}.key', 'wb') as file_key:
        file_key.write(key)

    click.echo(f"Key file {name}.key successfully generated!")
    click.echo("Save {name}.key somewhere secure, you will not be able to recover files encrypted using this key "
               "without it.")


@cli.command(name="encrypt")
@click.pass_context
@click.option("--filename", "-n", type=click.Path(exists=True), prompt="Relative path to file", help="The relative path"
                                                                                                     " to the file you "
                                                                                                     "want to encrypt.")
@click.option("--key", "-k", type=click.Path(exists=True), prompt="Relative path to key", help="The relative path to "
                                                                                               "the key you want to "
                                                                                               "use.")
def encrypt_file(ctx, filename, key):
    """Encrypt a file with an existing key"""

    click.echo(f"Encrypting {filename}...")

    # opening the key
    with open(key, 'rb') as file_key:
        key = file_key.read()

    # using the generated key
    fernet = Fernet(key)

    # opening the original file to encrypt
    with open(filename, 'rb') as file:
        original = file.read()

    # encrypting the file
    encrypted = fernet.encrypt(original)

    # opening the file in write mode and
    # writing the encrypted data
    with open(filename, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

    click.echo(f"{filename} encrypted successfully!")


@cli.command(name="decrypt")
@click.pass_context
@click.option("--filename", "-n", type=click.Path(exists=True), prompt="Relative path to file", help="The relative path"
                                                                                                     " to the file you "
                                                                                                     "want to decrypt.")
@click.option("--key", "-k", type=click.Path(exists=True), prompt="Relative path to key", help="The relative path to "
                                                                                               "the key you want to "
                                                                                               "use.")
def decrypt_file(ctx, filename, key):
    """Decrypt a file with a key"""

    click.echo(f"Decrypting {filename}...")

    # using the key
    with open(key, 'rb') as file_key:
        key = file_key.read()

    fernet = Fernet(key)

    # opening the encrypted file
    with open(filename, 'rb') as enc_file:
        encrypted = enc_file.read()

    # decrypting the file
    decrypted = fernet.decrypt(encrypted)

    # opening the file in write mode and
    # writing the decrypted data
    with open(filename, 'wb') as dec_file:
        dec_file.write(decrypted)

    click.echo(f"{filename} decrypted successfully!")


if __name__ == '__main__':
    cli()
