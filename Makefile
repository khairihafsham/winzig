reset-db:
	$(MAKE) -- compose "exec postgres.local psql -U postgres -c 'drop database if exists winzig'"
	$(MAKE) compose "exec postgres.local createdb winzig -U postgres"
	$(MAKE) -- compose run --rm web alembic upgrade head

compose:
	@docker-compose -f docker-compose.yaml -f docker-compose.dev.yaml \
		$(filter-out $@,$(MAKECMDGOALS))

unit_test:
	@$(MAKE) -- compose run --rm web py.test --cov .

behave:
	@$(MAKE) compose "exec web behave test/features"

test: unit_test behave

%:
	@:
