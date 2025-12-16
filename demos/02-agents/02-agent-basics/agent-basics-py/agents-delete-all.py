import os
import io
import sys
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import PromptAgentDefinition

# Configure UTF-8 encoding for Windows console (fixes emoji display issues)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def is_new_ms_foundry_endpoint(endpoint: str) -> bool:
    if not endpoint:
        return False
    endpoint_l = endpoint.lower()
    return (
        "foundry.microsoft.com" in endpoint_l
        or endpoint_l.startswith("https://api.foundry.")
        or ".foundry.microsoft.com" in endpoint_l
    )


def main():
    """Delete agents in the Azure AI Foundry project."""
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

    # Load env only; no flags. Use PROJECT_ENDPOINT.
    load_dotenv()
    endpoint = os.getenv("PROJECT_ENDPOINT")

    print(f"{'='*70}")
    print("🗑️  AGENT DELETION UTILITY")
    print(f"{'='*70}")
    print(f"Endpoint: {endpoint}")
    print()

    if not endpoint:
        print("❌ PROJECT_ENDPOINT not set and --endpoint not provided.")
        print("   Please provide a Classic Azure AI Foundry project endpoint.")
        sys.exit(1)

    # Operate on the given endpoint (Classic or Microsoft Foundry). No flags required.

    project_client = AIProjectClient(
        endpoint=endpoint,
        credential=DefaultAzureCredential(),
    )

    with project_client:
        # List all agents and their versions
        print("📋 Fetching all agents and versions...")
        agents = project_client.agents.list()

        agent_versions = []
        agent_counter = 0

        for agent in agents:
            try:
                versions = project_client.agents.list_versions(agent.name)
                for version in versions:
                    agent_counter += 1
                    # Extract model information
                    model_name = "Unknown"
                    if hasattr(version, 'model') and version.model:
                        model_name = version.model
                    elif hasattr(version, 'definition') and version.definition:
                        if hasattr(version.definition, 'model'):
                            model_name = version.definition.model

                    # Extract description
                    description = "No description"
                    if hasattr(version, 'description') and version.description:
                        description = version.description
                    elif hasattr(version, 'definition') and version.definition:
                        if hasattr(version.definition, 'instructions'):
                            desc = version.definition.instructions
                            if desc and len(desc) > 50:
                                description = desc[:47] + "..."
                            elif desc:
                                description = desc

                    # Determine if this is a Single Agent (prompt-based)
                    is_single = False
                    try:
                        # Best-effort detection: PromptAgentDefinition type or having 'instructions'
                        if isinstance(getattr(version, 'definition', None), PromptAgentDefinition):
                            is_single = True
                        elif hasattr(version, 'definition') and hasattr(version.definition, 'instructions'):
                            is_single = True
                    except Exception:
                        pass

                    agent_versions.append({
                        'number': agent_counter,
                        'agent_name': agent.name,
                        'version': version.version,
                        'model': model_name,
                        'description': description,
                        'is_single': is_single,
                    })
            except Exception as e:
                print(f"⚠️  Could not fetch versions for agent '{agent.name}': {e}")

        if not agent_versions:
            print("\n✅ No agent versions found. Nothing to delete.")
            print("   Ensure PROJECT_ENDPOINT points to your Microsoft Foundry project if you expect Single Agents.")
            return

        # Always restrict to Single (Declarative) Agents
        agent_versions = [av for av in agent_versions if av.get('is_single')]

        if not agent_versions:
            print("\n✅ No Single (declarative) agents found. Nothing to delete.")
            return

        print(f"\n📊 Found {len(agent_versions)} Single Agent version(s):")
        print(f"{'─'*100}")
        print(f"{'#':<3} {'Agent Name':<20} {'Version':<8} {'Model':<20} {'Description'}")
        print(f"{'─'*100}")

        for av in agent_versions:
            model_display = av['model'][:18] + '...' if len(av['model']) > 18 else av['model']
            desc_display = av['description'][:45] + '...' if len(av['description']) > 45 else av['description']
            print(f"{av['number']:<3} {av['agent_name']:<20} {av['version']:<8} {model_display:<20} {desc_display}")

        print(f"{'─'*100}")
        # Non-interactive: delete all listed Single Agent versions
        versions_to_delete = agent_versions

        print(f"\n🗑️  Deleting {len(versions_to_delete)} Single Agent version(s)...")

        print()
        print("🗑️  Deleting agent versions...")
        print(f"{'─'*70}")

        deleted_count = 0
        failed_count = 0
        affected_agents = set()

        for i, av in enumerate(versions_to_delete, 1):
            try:
                project_client.agents.delete_version(
                    agent_name=av['agent_name'],
                    agent_version=av['version']
                )
                print(f"✓ [{i}/{len(versions_to_delete)}] Deleted: {av['agent_name']}:{av['version']}")
                deleted_count += 1
                affected_agents.add(av['agent_name'])
            except Exception as e:
                print(f"✗ [{i}/{len(versions_to_delete)}] Failed to delete {av['agent_name']}:{av['version']}: {e}")
                failed_count += 1

        # Attempt to delete empty agent containers too (best-effort)
        print(f"{'─'*70}")
        print("🧹 Cleaning up empty agent containers (best effort)...")
        container_deleted = 0
        container_failed = 0
        for idx, agent_name in enumerate(sorted(affected_agents), 1):
            try:
                # Some SDK versions support deleting the agent container (no version argument)
                project_client.agents.delete(agent_name=agent_name)
                print(f"• [{idx}/{len(affected_agents)}] Deleted agent container: {agent_name}")
                container_deleted += 1
            except Exception as e:
                # Not all SDKs expose this; ignore failures
                print(f"• [{idx}/{len(affected_agents)}] Could not delete agent container {agent_name}: {e}")
                container_failed += 1

        print(f"{'─'*70}")
        print()
        print(f"{'='*70}")
        print("📊 SUMMARY")
        print(f"{'='*70}")
        print(f"✅ Successfully deleted: {deleted_count} agent version(s)")
        if failed_count > 0:
            print(f"❌ Failed to delete: {failed_count} agent version(s)")
        if container_deleted or container_failed:
            print(f"🧹 Agent containers deleted: {container_deleted}; failed: {container_failed}")
        print(f"{'='*70}")


if __name__ == '__main__':
    main()
